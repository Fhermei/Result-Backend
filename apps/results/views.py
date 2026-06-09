from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.utils import timezone

from .models import Result, SemesterGPARecord, CGPARecord
from .serializers import (
    ResultSerializer, ResultCreateSerializer, ResultUpdateSerializer,
    BulkResultCreateSerializer, SemesterGPASerializer, CGPASerializer
)
from apps.accounts.permissions import IsAdmin, IsLecturer, IsStudent, IsAdminOrLecturer
from apps.students.models import StudentProfile
from apps.academics.models import Semester
from apps.courses.models import Course


# GPA Calculation Functions
GRADE_POINTS = {
    'A': 5.0,
    'B': 4.0,
    'C': 3.0,
    'D': 2.0,
    'E': 1.0,
    'F': 0.0,
}

def calculate_semester_gpa(results_data):
    """Calculate GPA from results data"""
    total_quality_points = 0
    total_credit_units = 0
    
    for result in results_data:
        credit_unit = result['credit_unit']
        grade = result['grade']
        
        quality_points = credit_unit * GRADE_POINTS.get(grade, 0)
        total_quality_points += quality_points
        total_credit_units += credit_unit
    
    if total_credit_units == 0:
        return 0.0, 0, 0
    
    gpa = total_quality_points / total_credit_units
    return round(gpa, 2), total_quality_points, total_credit_units


def calculate_cgpa(semester_data):
    """Calculate CGPA across multiple semesters"""
    total_quality_points_all = sum(s['total_quality_points'] for s in semester_data)
    total_credit_units_all = sum(s['total_credit_units'] for s in semester_data)
    
    if total_credit_units_all == 0:
        return 0.0
    
    cgpa = total_quality_points_all / total_credit_units_all
    return round(cgpa, 2)


def get_class_degree(cgpa):
    """Get degree classification based on CGPA"""
    if cgpa >= 4.50:
        return 'First Class'
    elif cgpa >= 3.50:
        return 'Second Class Upper'
    elif cgpa >= 2.40:
        return 'Second Class Lower'
    elif cgpa >= 1.50:
        return 'Third Class'
    elif cgpa >= 1.00:
        return 'Pass'
    else:
        return 'Probation'


class ResultListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrLecturer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'course', 'semester', 'is_published']
    search_fields = ['student__matric_no', 'course__code', 'course__title']
    ordering_fields = ['created_at', 'total_score']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResultCreateSerializer
        return ResultSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Result.objects.select_related('student', 'course', 'semester').all()
        elif user.is_lecturer:
            return Result.objects.filter(
                course__lecturer=user
            ).select_related('student', 'course', 'semester')
        return Result.objects.none()


class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrLecturer]
    queryset = Result.objects.select_related('student', 'course', 'semester').all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResultUpdateSerializer
        return ResultSerializer

class BulkResultUploadView(APIView):
    """Lecturer bulk uploads results for a course"""
    permission_classes = [IsAuthenticated, IsLecturer]
    
    def post(self, request):
        print("=" * 60)
        print("BULK UPLOAD - START")
        print("=" * 60)
        print(f"Request user: {request.user.email}")
        print(f"Request data: {request.data}")
        
        serializer = BulkResultCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        semester_id = data['semester_id']
        results_data = data['results']
        
        print(f"Semester ID: {semester_id}")
        print(f"Number of results: {len(results_data)}")
        
        try:
            semester = Semester.objects.get(id=semester_id)
            print(f"Semester found: {semester} (ID: {semester.id})")
        except Semester.DoesNotExist:
            print(f"ERROR: Semester {semester_id} not found")
            return Response({'error': 'Semester not found'}, status=404)
        
        created_results = []
        errors = []
        
        with transaction.atomic():
            for idx, result_item in enumerate(results_data):
                try:
                    student_id = result_item.get('student_id')
                    course_id = result_item.get('course_id')
                    ca_score = result_item.get('ca_score')
                    exam_score = result_item.get('exam_score')
                    
                    print(f"\n--- Result {idx+1} ---")
                    print(f"Student ID: {student_id}, Course ID: {course_id}")
                    
                    student = StudentProfile.objects.get(id=student_id)
                    print(f"Student found: {student.matric_no}")
                    
                    course = Course.objects.get(id=course_id)
                    print(f"Course found: {course.code} - {course.title}")
                    
                    # Create or update result
                    result, created = Result.objects.update_or_create(
                        student=student,
                        course=course,
                        semester=semester,
                        defaults={
                            'ca_score': ca_score,
                            'exam_score': exam_score,
                            'is_published': True  # Auto-publish for now
                        }
                    )
                    
                    if created:
                        print(f"  CREATED new result ID: {result.id}")
                    else:
                        print(f"  UPDATED existing result ID: {result.id}")
                    
                    created_results.append(result)
                    
                except StudentProfile.DoesNotExist:
                    error_msg = f"Student ID {student_id} not found"
                    errors.append(error_msg)
                    print(f"  ERROR: {error_msg}")
                except Course.DoesNotExist:
                    error_msg = f"Course ID {course_id} not found"
                    errors.append(error_msg)
                    print(f"  ERROR: {error_msg}")
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    errors.append(error_msg)
                    print(f"  ERROR: {error_msg}")
        
        print("\n" + "=" * 60)
        print("BULK UPLOAD - COMPLETE")
        print(f"Created/Updated: {len(created_results)}")
        print(f"Errors: {len(errors)}")
        print("=" * 60)
        
        # After saving, verify the results exist
        verify_results = Result.objects.filter(
            semester=semester,
            course__in=[r.course for r in created_results]
        )
        print(f"VERIFICATION: {verify_results.count()} results found in DB for this semester/course")
        
        return Response({
            'message': f'Successfully processed {len(created_results)} results',
            'errors': errors,
            'results': ResultSerializer(created_results, many=True).data
        }, status=status.HTTP_201_CREATED)

class MyResultsView(generics.ListAPIView):
    """Student views their own results"""
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['semester']
    
    def get_queryset(self):
        try:
            student = StudentProfile.objects.get(user=self.request.user)
            return Result.objects.filter(
                student=student,
                is_published=True
            ).select_related('course', 'semester')
        except StudentProfile.DoesNotExist:
            return Result.objects.none()


class SemesterGPAView(generics.ListAPIView):
    """Get GPA for a student per semester"""
    permission_classes = [IsAuthenticated]
    serializer_class = SemesterGPASerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            student_id = self.request.query_params.get('student_id')
            if student_id:
                return SemesterGPARecord.objects.filter(student_id=student_id)
            return SemesterGPARecord.objects.all()
        elif user.is_student:
            try:
                student = StudentProfile.objects.get(user=user)
                return SemesterGPARecord.objects.filter(student=student)
            except StudentProfile.DoesNotExist:
                return SemesterGPARecord.objects.none()
        return SemesterGPARecord.objects.none()


class CalculateGPAView(APIView):
    """Calculate GPA for a student in a semester and store it"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        semester_id = request.data.get('semester_id')
        
        if not student_id or not semester_id:
            return Response({'error': 'student_id and semester_id required'}, status=400)
        
        try:
            student = StudentProfile.objects.get(id=student_id)
            semester = Semester.objects.get(id=semester_id)
        except (StudentProfile.DoesNotExist, Semester.DoesNotExist):
            return Response({'error': 'Student or Semester not found'}, status=404)
        
        # Get all published results for this student in this semester
        results = Result.objects.filter(
            student=student,
            semester=semester,
            is_published=True
        ).select_related('course')
        
        if not results:
            return Response({'error': 'No published results found'}, status=404)
        
        # Prepare data for GPA calculation
        results_data = []
        for result in results:
            results_data.append({
                'credit_unit': result.course.credit_unit,
                'total_score': float(result.total_score),
                'grade': result.grade
            })
        
        # Calculate GPA
        gpa, total_qp, total_cu = calculate_semester_gpa(results_data)
        class_degree = get_class_degree(gpa)
        
        # Store in database
        gpa_record, created = SemesterGPARecord.objects.update_or_create(
            student=student,
            semester=semester,
            defaults={
                'gpa': gpa,
                'total_quality_points': total_qp,
                'total_credit_units': total_cu,
                'class_degree': class_degree
            }
        )
        
        return Response({
            'student': student.matric_no,
            'semester': str(semester),
            'gpa': gpa,
            'total_quality_points': total_qp,
            'total_credit_units': total_cu,
            'class_degree': class_degree,
            'created': created
        })


class CalculateCGPAView(APIView):
    """Calculate CGPA for a student across all semesters"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        
        if not student_id:
            return Response({'error': 'student_id required'}, status=400)
        
        try:
            student = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        
        # Get all GPA records for this student
        gpa_records = SemesterGPARecord.objects.filter(student=student)
        
        if not gpa_records:
            return Response({'error': 'No GPA records found. Run GPA calculation first.'}, status=404)
        
        # Calculate CGPA
        semester_data = []
        for record in gpa_records:
            semester_data.append({
                'total_quality_points': float(record.total_quality_points),
                'total_credit_units': record.total_credit_units
            })
        
        cgpa = calculate_cgpa(semester_data)
        class_degree = get_class_degree(cgpa)
        
        # Calculate totals
        total_qp = sum(float(r.total_quality_points) for r in gpa_records)
        total_cu = sum(r.total_credit_units for r in gpa_records)
        
        # Store in database
        cgpa_record, created = CGPARecord.objects.update_or_create(
            student=student,
            defaults={
                'cgpa': cgpa,
                'total_quality_points_all': total_qp,
                'total_credit_units_all': total_cu,
                'class_degree': class_degree
            }
        )
        
        return Response({
            'student': student.matric_no,
            'cgpa': cgpa,
            'total_quality_points': total_qp,
            'total_credit_units': total_cu,
            'class_degree': class_degree
        })


class PublishResultsView(APIView):
    """Admin publishes results"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        semester_id = request.data.get('semester_id')
        
        if not semester_id:
            return Response({'error': 'semester_id required'}, status=400)
        
        try:
            semester = Semester.objects.get(id=semester_id)
        except Semester.DoesNotExist:
            return Response({'error': 'Semester not found'}, status=404)
        
        # Get all unpublished results for this semester
        results = Result.objects.filter(semester=semester, is_published=False)
        
        if not results:
            return Response({'message': 'No unpublished results found for this semester'})
        
        published_count = 0
        for result in results:
            result.is_published = True
            result.published_at = timezone.now()
            result.save()
            published_count += 1
        
        # Update semester publish status
        semester.is_result_published = True
        semester.save()
        
        return Response({
            'message': f'Successfully published {published_count} results',
            'semester': str(semester)
        })


class TranscriptView(APIView):
    """Generate student transcript"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id=None):
        user = request.user
        
        if user.is_student:
            try:
                student = StudentProfile.objects.get(user=user)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)
        elif user.is_admin and student_id:
            try:
                student = StudentProfile.objects.get(id=student_id)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student not found'}, status=404)
        else:
            return Response({'error': 'Permission denied'}, status=403)
        
        # Get GPA records
        gpa_records = SemesterGPARecord.objects.filter(student=student).select_related('semester')
        
        # Get CGPA
        try:
            cgpa_record = CGPARecord.objects.get(student=student)
        except CGPARecord.DoesNotExist:
            cgpa_record = None
        
        # Get all results
        results = Result.objects.filter(
            student=student,
            is_published=True
        ).select_related('course', 'semester')
        
        transcript_data = {
            'student_id': student.id,
            'student_name': student.user.get_full_name(),
            'matric_no': student.matric_no,
            'department': student.department.name,
            'faculty': student.department.faculty.name,
            'admission_year': student.admission_year,
            'cgpa': float(cgpa_record.cgpa) if cgpa_record else 0,
            'class_degree': cgpa_record.class_degree if cgpa_record else 'Not Available',
            'semesters': SemesterGPASerializer(gpa_records, many=True).data,
            'courses': ResultSerializer(results, many=True).data
        }
        
        return Response(transcript_data)