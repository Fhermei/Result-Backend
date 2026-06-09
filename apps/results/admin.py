from django.contrib import admin
from .models import Result, SemesterGPARecord, CGPARecord, ResultVerification


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'total_score', 'grade', 'is_published']
    list_filter = ['semester', 'is_published', 'grade']
    search_fields = ['student__matric_no', 'course__code']
    readonly_fields = ['total_score', 'grade', 'quality_points']


@admin.register(SemesterGPARecord)
class SemesterGPARecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'gpa', 'class_degree']
    list_filter = ['semester']


@admin.register(CGPARecord)
class CGPARecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'cgpa', 'class_degree']
    search_fields = ['student__matric_no']


@admin.register(ResultVerification)
class ResultVerificationAdmin(admin.ModelAdmin):
    list_display = ['student', 'is_verified', 'verified_at']