from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, CourseRegistration
from .serializers import CourseSerializer, CourseRegistrationSerializer
from apps.accounts.permissions import IsAdmin, IsAdminOrLecturer, IsStudent, IsLecturer
from apps.students.models import StudentProfile
from apps.academics.models import Semester
from apps.students.serializers import StudentProfileSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    """List courses - accessible by all authenticated users, create only by admin/lecturer"""
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'level', 'semester', 'is_elective', 'lecturer']
    search_fields = ['code', 'title']
    ordering_fields = ['code', 'title', 'credit_unit']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            # Anyone authenticated can view courses
            return [IsAuthenticated()]
        # POST, PUT, DELETE require admin or lecturer
        return [IsAdminOrLecturer()]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.select_related('department', 'level', 'semester', 'lecturer')
        
        # For students, show only courses at their level
        if user.is_student:
            try:
                student = StudentProfile.objects.get(user=user)
                return queryset.filter(level=student.current_level)
            except StudentProfile.DoesNotExist:
                return queryset.none()
        
        return queryset


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.select_related('department', 'level', 'semester', 'lecturer').all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminOrLecturer()]


class MyCoursesView(generics.ListAPIView):
    """Lecturer sees their assigned courses. Student sees registered courses."""
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_lecturer:
            return Course.objects.filter(lecturer=user).select_related('department', 'level', 'semester')
        elif user.is_student:
            try:
                student = StudentProfile.objects.get(user=user)
                current_semester = Semester.get_current()
                registered_courses = CourseRegistration.objects.filter(
                    student=student, 
                    semester=current_semester
                ).values_list('course', flat=True)
                return Course.objects.filter(id__in=registered_courses)
            except StudentProfile.DoesNotExist:
                return Course.objects.none()
        return Course.objects.none()


class RegisterCoursesView(generics.CreateAPIView):
    """Student registers for courses for the current semester"""
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CourseRegistrationSerializer
    
    def post(self, request):
        user = request.user
        try:
            student = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=400)
        
        current_semester = Semester.get_current()
        if not current_semester:
            return Response({'error': 'No active semester'}, status=400)
        
        course_ids = request.data.get('course_ids', [])
        if not course_ids:
            return Response({'error': 'No courses selected'}, status=400)
        
        registrations = []
        errors = []
        
        for course_id in course_ids:
            try:
                course = Course.objects.get(id=course_id, level=student.current_level, semester=current_semester)
                registration, created = CourseRegistration.objects.get_or_create(
                    student=student,
                    course=course,
                    semester=current_semester
                )
                if created:
                    registrations.append(registration)
            except Course.DoesNotExist:
                errors.append(f'Course ID {course_id} not available for your level this semester')
        
        serializer = CourseRegistrationSerializer(registrations, many=True)
        return Response({
            'message': f'Successfully registered for {len(registrations)} courses',
            'errors': errors,
            'registrations': serializer.data
        }, status=status.HTTP_201_CREATED)


class MyRegisteredCoursesView(generics.ListAPIView):
    """Student sees their registered courses for current semester"""
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CourseRegistrationSerializer
    
    def get_queryset(self):
        user = self.request.user
        try:
            student = StudentProfile.objects.get(user=user)
            current_semester = Semester.get_current()
            return CourseRegistration.objects.filter(
                student=student, 
                semester=current_semester
            ).select_related('course', 'course__department')
        except StudentProfile.DoesNotExist:
            return CourseRegistration.objects.none()


class CourseStudentsView(generics.ListAPIView):
    """Get all students enrolled in a course (for lecturers)"""
    permission_classes = [IsAuthenticated, IsLecturer]
    serializer_class = StudentProfileSerializer
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return StudentProfile.objects.none()
        
        # Verify lecturer teaches this course
        if self.request.user != course.lecturer and not self.request.user.is_admin:
            return StudentProfile.objects.none()
        
        # Get students registered for this course
        registrations = CourseRegistration.objects.filter(course=course)
        student_ids = registrations.values_list('student', flat=True)
        
        return StudentProfile.objects.filter(id__in=student_ids).select_related('user', 'department', 'current_level')