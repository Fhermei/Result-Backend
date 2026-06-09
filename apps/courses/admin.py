from django.contrib import admin
from .models import Course, CourseRegistration


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'credit_unit', 'department', 'level', 'semester', 'lecturer']
    list_filter = ['department', 'level', 'semester', 'is_elective']
    search_fields = ['code', 'title']


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'registered_at']
    list_filter = ['semester', 'course__department']
    search_fields = ['student__matric_no', 'course__code']