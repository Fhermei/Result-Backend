from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['matric_no', 'user', 'department', 'current_level', 'admission_year', 'is_graduated']
    list_filter = ['department', 'current_level', 'is_graduated']
    search_fields = ['matric_no', 'user__first_name', 'user__last_name', 'user__email']