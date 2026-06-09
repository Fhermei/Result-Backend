from rest_framework import serializers
from .models import StudentProfile
from apps.accounts.serializers import UserDetailSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    user_details = UserDetailSerializer(source='user', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    current_level_value = serializers.IntegerField(source='current_level.level', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'user_details', 'full_name', 'email', 'matric_no',
                  'department', 'department_name', 'department_code', 'current_level',
                  'current_level_value', 'admission_year', 'is_graduated', 'created_at']


class CreateStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    matric_no = serializers.CharField(max_length=20)
    department_id = serializers.IntegerField()
    level_id = serializers.IntegerField()
    admission_year = serializers.IntegerField()
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs