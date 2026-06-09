from rest_framework import serializers
from .models import Course, CourseRegistration
from apps.academics.serializers import DepartmentSerializer, LevelSerializer, SemesterSerializer


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    level_value = serializers.IntegerField(source='level.level', read_only=True)
    semester_name = serializers.CharField(source='semester.get_name_display', read_only=True)
    lecturer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'credit_unit', 'department', 'department_name', 
                  'department_code', 'level', 'level_value', 'semester', 'semester_name',
                  'lecturer', 'lecturer_name', 'is_elective', 'created_at']
    
    def get_lecturer_name(self, obj):
        if obj.lecturer:
            return obj.lecturer.get_full_name()
        return None


class CourseRegistrationSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = CourseRegistration
        fields = ['id', 'student', 'course', 'course_details', 'semester', 'registered_at']