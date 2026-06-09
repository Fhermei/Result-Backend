from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.students.models import StudentProfile
from apps.courses.models import Course
from apps.academics.models import Semester
import hashlib
import json


def calculate_grade(score):
    """Calculate letter grade based on score (0-100)"""
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    elif score >= 40:
        return 'E'
    else:
        return 'F'


def calculate_quality_points(credit_unit, grade):
    """Calculate quality points for a course"""
    grade_points = {
        'A': 5.0,
        'B': 4.0,
        'C': 3.0,
        'D': 2.0,
        'E': 1.0,
        'F': 0.0,
    }
    return credit_unit * grade_points.get(grade, 0)


class Result(models.Model):
    """Individual course result for a student in a semester"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='results')
    
    # Scores (CA = Continuous Assessment, typically 30-40%, Exam = 60-70%)
    ca_score = models.DecimalField(max_digits=5, decimal_places=2, 
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    exam_score = models.DecimalField(max_digits=5, decimal_places=2,
                                     validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Calculated fields
    total_score = models.DecimalField(max_digits=5, decimal_places=2, editable=False, default=0)
    grade = models.CharField(max_length=1, editable=False, default='F')
    quality_points = models.DecimalField(max_digits=5, decimal_places=2, editable=False, default=0)
    
    # Blockchain
    blockchain_hash = models.CharField(max_length=66, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course', 'semester']
        ordering = ['course__code']
    
    def save(self, *args, **kwargs):
        # Calculate total score (CA + Exam)
        self.total_score = self.ca_score + self.exam_score
        
        # Calculate grade and quality points
        self.grade = calculate_grade(float(self.total_score))
        self.quality_points = calculate_quality_points(self.course.credit_unit, self.grade)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.student.matric_no} - {self.course.code}: {self.grade}'


class SemesterGPARecord(models.Model):
    """Stores calculated GPA for a student per semester"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='gpa_records')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total_quality_points = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_credit_units = models.PositiveIntegerField(default=0)
    class_degree = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'semester']
        ordering = ['semester__session__name', 'semester__name']
    
    def __str__(self):
        return f'{self.student.matric_no} - {self.semester}: GPA {self.gpa}'


class CGPARecord(models.Model):
    """Stores cumulative CGPA for a student"""
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='cgpa_record')
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total_quality_points_all = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_credit_units_all = models.PositiveIntegerField(default=0)
    class_degree = models.CharField(max_length=50, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.student.matric_no}: CGPA {self.cgpa} ({self.class_degree})'


class ResultVerification(models.Model):
    """Tracks result verification requests"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='verifications')
    result_hash = models.CharField(max_length=66)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'Verification for {self.student.matric_no}: {self.is_verified}'