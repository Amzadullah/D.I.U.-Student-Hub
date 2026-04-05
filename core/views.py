from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import LostItem, Complaint
import google.generativeai as genai
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

DIU_SYSTEM_PROMPT = """
তুমি DIU (Daffodil International University) এর একজন helpful AI assistant।
তুমি শুধু DIU সম্পর্কিত প্রশ্নের উত্তর দেবে বাংলায়।

DIU সম্পর্কে তুমি যা জানো:
- Location: Dhanmondi, Dhaka এবং Ashulia permanent campus
- Departments: CSE, EEE, BBA, English, Law, Pharmacy, Architecture and more
- Library: রবি-বৃহস্পতি ৮AM-৮PM, শনি ৯AM-৪PM
- Portal: portal.daffodilvarsity.edu.bd
- Helpline: 09617930234
- CGPA: A+=4.0, A=3.75, A-=3.5, B+=3.25, B=3.0, B-=2.75, C+=2.5, C=2.25, D=2.0, F=0

নতুন students দের জন্য গুরুত্বপূর্ণ তথ্য:
- প্রথম দিন: Student ID card সংগ্রহ করো Registrar office থেকে
- Portal এ login করতে Student ID ও date of birth ব্যবহার করো
- Class routine portal এ পাওয়া যায়
- Semester fee deadline miss করলে late fee দিতে হয়

সবসময় friendly, helpful এবং সংক্ষিপ্ত উত্তর দাও।
"""

def homepage(request):
    lost_count = LostItem.objects.filter(is_found=False).count()
    found_count = LostItem.objects.filter(is_found=True).count()
    return render(request, 'core/home.html', {
        'lost_count': lost_count,
        'found_count': found_count,
    })

def lost_and_found(request):
    query = request.GET.get('q', '')
    if query:
        items = LostItem.objects.filter(title__icontains=query) | LostItem.objects.filter(description__icontains=query)
    else:
        items = LostItem.objects.all().order_by('-date_posted')
    return render(request, 'core/lost_found.html', {'items': items, 'query': query})

def post_item(request):
    if request.method == 'POST':
        LostItem.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            contact=request.POST.get('contact', ''),
            image=request.FILES.get('image'),
            is_found=request.POST.get('is_found') == 'on',
        )
        return redirect('lost_found')
    return render(request, 'core/post_item.html')

def ai_chat_page(request):
    return render(request, 'core/ai_chat.html')

@csrf_exempt
def ai_chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        history = data.get('history', [])
        try:
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=DIU_SYSTEM_PROMPT
            )
            chat_history = []
            for h in history[-6:]:
                chat_history.append({'role': h['role'], 'parts': [h['content']]})
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_message)
            return JsonResponse({'reply': response.text})
        except Exception as e:
            return JsonResponse({'reply': f'Sorry, error হয়েছে: {str(e)}'})
    return JsonResponse({'error': 'Invalid'}, status=400)

def complaint_page(request):
    if request.method == 'POST':
        text = request.POST['complaint_text'].lower()
        if any(w in text for w in ['wifi', 'internet', 'computer', 'lab', 'network']):
            dept = 'IT'
        elif any(w in text for w in ['hall', 'hostel', 'room', 'থাকা', 'dormitory']):
            dept = 'PROVOST'
        elif any(w in text for w in ['result', 'exam', 'cgpa', 'পরীক্ষা', 'grade']):
            dept = 'EXAM'
        elif any(w in text for w in ['fee', 'payment', 'টাকা', 'ফি', 'accounts']):
            dept = 'ACCOUNTS'
        elif any(w in text for w in ['teacher', 'class', 'course', 'শিক্ষক', 'syllabus']):
            dept = 'ACADEMIC'
        else:
            dept = 'STUDENT_AFFAIRS'

        Complaint.objects.create(
            name=request.POST['name'],
            student_id=request.POST['student_id'],
            complaint_text=request.POST['complaint_text'],
            routed_to=dept,
        )
        return render(request, 'core/complaint.html', {'submitted': True, 'dept': dict(Complaint.DEPARTMENT_CHOICES)[dept]})
    return render(request, 'core/complaint.html')