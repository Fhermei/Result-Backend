from rest_framework import serializers
from .models import Result, SemesterGPARecord, CGPARecord
from apps.courses.serializers import CourseSerializer
from apps.academics.serializers import SemesterSerializer


# Grade points mapping
GRADE_POINTS = {
    'A': 5.0,
    'B': 4.0,
    'C': 3.0,
    'D': 2.0,
    'E': 1.0,
    'F': 0.0,
}


class ResultSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    semester_details = SemesterSerializer(source='semester', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_matric = serializers.CharField(source='student.matric_no', read_only=True)
    grade_point = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Result
        fields = ['id', 'student', 'student_name', 'student_matric', 'course', 'course_details',
                  'semester', 'semester_details', 'ca_score', 'exam_score', 'total_score',
                  'grade', 'grade_point', 'quality_points', 'is_published', 'blockchain_hash',
                  'status', 'published_at', 'created_at']
        read_only_fields = ['total_score', 'grade', 'quality_points']
    
    def get_grade_point(self, obj):
        return GRADE_POINTS.get(obj.grade, 0)
    
    def get_status(self, obj):
        if obj.blockchain_hash:
            return 'Verified on Blockchain'
        elif obj.is_published:
            return 'Published (Pending Blockchain)'
        return 'Draft'


class ResultCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new results"""
    
    class Meta:
        model = Result
        fields = ['student', 'course', 'semester', 'ca_score', 'exam_score']
    
    def validate(self, data):
        # Check if result already exists
        if Result.objects.filter(
            student=data['student'],
            course=data['course'],
            semester=data['semester']
        ).exists():
            raise serializers.ValidationError('Result already exists for this student, course, and semester')
        
        # Validate score ranges
        if data.get('ca_score', 0) < 0 or data.get('ca_score', 0) > 40:
            raise serializers.ValidationError({'ca_score': 'CA score must be between 0 and 40'})
        if data.get('exam_score', 0) < 0 or data.get('exam_score', 0) > 70:
            raise serializers.ValidationError({'exam_score': 'Exam score must be between 0 and 70'})
        
        return data


class ResultUpdateSerializer(serializers.ModelSerializer):
    """Serializer specifically for updating results (only allows score updates)"""
    
    class Meta:
        model = Result
        fields = ['ca_score', 'exam_score']
    
    def validate(self, data):
        # Validate that scores are within range
        if data.get('ca_score', 0) > 40:
            raise serializers.ValidationError({'ca_score': 'CA score cannot exceed 40'})
        if data.get('exam_score', 0) > 70:
            raise serializers.ValidationError({'exam_score': 'Exam score cannot exceed 70'})
        if data.get('ca_score', 0) < 0:
            raise serializers.ValidationError({'ca_score': 'CA score cannot be negative'})
        if data.get('exam_score', 0) < 0:
            raise serializers.ValidationError({'exam_score': 'Exam score cannot be negative'})
        return data


class BulkResultCreateSerializer(serializers.Serializer):
    """For lecturers to bulk upload results"""
    semester_id = serializers.IntegerField()
    results = serializers.ListField(
        child=serializers.DictField()
    )
    
    def validate_results(self, value):
        for item in value:
            if 'student_id' not in item:
                raise serializers.ValidationError('Each result must have student_id')
            if 'course_id' not in item:
                raise serializers.ValidationError('Each result must have course_id')
            if 'ca_score' not in item:
                raise serializers.ValidationError('Each result must have ca_score')
            if 'exam_score' not in item:
                raise serializers.ValidationError('Each result must have exam_score')
            
            # Validate score ranges
            ca_score = item.get('ca_score')
            exam_score = item.get('exam_score')
            if ca_score < 0 or ca_score > 40:
                raise serializers.ValidationError(f'CA score for student {item.get("student_id")} must be between 0 and 40')
            if exam_score < 0 or exam_score > 70:
                raise serializers.ValidationError(f'Exam score for student {item.get("student_id")} must be between 0 and 70')
        
        return value


class SemesterGPASerializer(serializers.ModelSerializer):
    semester_details = SemesterSerializer(source='semester', read_only=True)
    
    class Meta:
        model = SemesterGPARecord
        fields = ['id', 'student', 'semester', 'semester_details', 'gpa', 
                  'total_quality_points', 'total_credit_units', 'class_degree',
                  'created_at']


class CGPASerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_matric = serializers.CharField(source='student.matric_no', read_only=True)
    department = serializers.CharField(source='student.department.name', read_only=True)
    
    class Meta:
        model = CGPARecord
        fields = ['id', 'student', 'student_name', 'student_matric', 'department',
                  'cgpa', 'total_quality_points_all', 'total_credit_units_all',
                  'class_degree', 'updated_at']