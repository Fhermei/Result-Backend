from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import StudentProfile
from .serializers import StudentProfileSerializer, CreateStudentSerializer
from apps.accounts.permissions import IsAdmin

User = get_user_model()


class StudentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'current_level', 'is_graduated']
    search_fields = ['matric_no', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['matric_no', 'admission_year']
    
    def get_queryset(self):
        return StudentProfile.objects.select_related('user', 'department', 'current_level').all()
    
    def create(self, request, *args, **kwargs):
        serializer = CreateStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Create user
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone', ''),
            role='student'
        )
        
        # Create student profile
        student = StudentProfile.objects.create(
            user=user,
            matric_no=data['matric_no'],
            department_id=data['department_id'],
            current_level_id=data['level_id'],
            admission_year=data['admission_year']
        )
        
        return Response(StudentProfileSerializer(student).data, status=status.HTTP_201_CREATED)


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = StudentProfile.objects.select_related('user', 'department', 'current_level').all()
    serializer_class = StudentProfileSerializer


class MyStudentProfileView(generics.RetrieveAPIView):
    """Student views their own profile"""
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileSerializer
    
    def get_object(self):
        user = self.request.user
        return StudentProfile.objects.get(user=user)