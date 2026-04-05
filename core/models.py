from django.db import models

class LostItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_found = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Complaint(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'IT Department'),
        ('EXAM', 'Exam Controller'),
        ('ACCOUNTS', 'Accounts Department'),
        ('PROVOST', 'Provost Office'),
        ('ACADEMIC', 'Department Head'),
        ('STUDENT_AFFAIRS', 'Student Affairs'),
    ]
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    complaint_text = models.TextField()
    routed_to = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_id} - {self.routed_to}"