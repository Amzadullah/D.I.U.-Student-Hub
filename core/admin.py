from django.contrib import admin
from .models import LostItem, Complaint

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'is_found', 'date_posted']
    list_filter = ['is_found']
    search_fields = ['title', 'description']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'routed_to', 'is_resolved', 'date_submitted']
    list_filter = ['routed_to', 'is_resolved']