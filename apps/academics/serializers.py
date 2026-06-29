from rest_framework import serializers
from .models import Faculty, Department, AcademicSession, Semester, Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'level']


class FacultySerializer(serializers.ModelSerializer):
    department_count = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'code', 'department_count', 'created_at']

    def get_department_count(self, obj):
        return obj.departments.count()


class DepartmentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    faculty_code = serializers.CharField(source='faculty.code', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'faculty', 'faculty_name', 'faculty_code', 'name', 'code', 'created_at']


class SemesterSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)
    name_display = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = Semester
        fields = [
            'id', 'session', 'session_name', 'name', 'name_display',
            'is_current', 'is_result_published', 'created_at',
        ]


class AcademicSessionSerializer(serializers.ModelSerializer):
    semesters = SemesterSerializer(many=True, read_only=True)

    class Meta:
        model = AcademicSession
        fields = ['id', 'name', 'is_current', 'start_date', 'end_date', 'semesters', 'created_at']