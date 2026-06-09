from django.db import models
from apps.academics.models import Department, Level, Semester


class Course(models.Model):
    # Course Information
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    credit_unit = models.PositiveIntegerField(default=3)
    
    # Relationships
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='courses')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    
    # Optional
    lecturer = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, 
                                 null=True, blank=True, limit_choices_to={'role': 'lecturer'},
                                 related_name='courses_taught')
    
    is_elective = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
        unique_together = ['code', 'department', 'semester']
    
    def __str__(self):
        return f'{self.code} - {self.title} ({self.credit_unit} units)'


class CourseRegistration(models.Model):
    """Tracks which courses a student registered for in a semester"""
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='course_registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course', 'semester']
    
    def __str__(self):
        return f'{self.student} - {self.course.code}'