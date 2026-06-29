from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import StudentProfile
from .serializers import StudentProfileSerializer, CreateStudentSerializer
from apps.accounts.permissions import IsAdmin

User = get_user_model()


class StudentListCreateView(generics.ListCreateAPIView):
    """
    List all students (Admin only) or Create a new student (Public for registration)
    """
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'current_level', 'is_graduated']
    search_fields = ['matric_no', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['matric_no', 'admission_year']

    def get_permissions(self):
        """
        Allow public access for POST (registration), require admin for GET
        """
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]

    def get_queryset(self):
        """
        Return all student profiles with related user data
        """
        try:
            return StudentProfile.objects.select_related(
                'user', 'department', 'current_level'
            ).all()
        except Exception as e:
            print(f"Error in get_queryset: {e}")
            return StudentProfile.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = CreateStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Check for duplicate email before trying to create
        if User.objects.filter(email__iexact=data['email']).exists():
            return Response(
                {'email': [f'A user with the email "{data["email"]}" already exists.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for duplicate matric_no
        if StudentProfile.objects.filter(matric_no=data['matric_no']).exists():
            return Response(
                {'matric_no': [f'A student with matric number "{data["matric_no"]}" already exists.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Create the user account
            user = User.objects.create_user(
                email=data['email'].lower(),
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data.get('phone', ''),
                role='student',
            )

            # Create the student profile
            student = StudentProfile.objects.create(
                user=user,
                matric_no=data['matric_no'],
                department_id=data['department_id'],
                current_level_id=data['level_id'],
                admission_year=data['admission_year'],
            )

            return Response(
                StudentProfileSerializer(student).data,
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError as e:
            error_str = str(e).lower()
            if 'matric_no' in error_str:
                return Response(
                    {'matric_no': ['That matric number is already in use.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if 'email' in error_str:
                return Response(
                    {'email': ['That email address is already in use.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {'detail': 'Could not create student due to a database conflict.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"Error creating student: {e}")
            return Response(
                {'detail': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = StudentProfile.objects.select_related(
        'user', 'department', 'current_level'
    ).all()
    serializer_class = StudentProfileSerializer


class MyStudentProfileView(generics.RetrieveAPIView):
    """Student views their own profile."""
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileSerializer

    def get_object(self):
        try:
            return StudentProfile.objects.get(user=self.request.user)
        except StudentProfile.DoesNotExist:
            return None