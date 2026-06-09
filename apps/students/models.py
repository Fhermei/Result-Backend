from django.db import models
from django.core.exceptions import ValidationError
from apps.academics.models import Department, Level


class StudentProfile(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='student_profile')
    matric_no = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='students')
    admission_year = models.IntegerField()
    is_graduated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['matric_no']
    
    def __str__(self):
        return f'{self.matric_no} - {self.user.get_full_name()}'
    
    def clean(self):
        if self.user.role != 'student':
            raise ValidationError('User must have student role')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)