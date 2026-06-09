from django.contrib import admin
from .models import Faculty, Department, AcademicSession, Semester, Level


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'faculty']
    list_filter = ['faculty']
    search_fields = ['name', 'code']


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_current', 'start_date', 'end_date']
    list_filter = ['is_current']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_current', 'is_result_published']
    list_filter = ['is_current', 'is_result_published', 'name']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level']