from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Faculty, Department, AcademicSession, Semester, Level
from .serializers import (
    FacultySerializer, DepartmentSerializer,
    AcademicSessionSerializer, SemesterSerializer, LevelSerializer,
)
from apps.accounts.permissions import IsAdminOrReadOnly


class FacultyListCreateView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class FacultyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class DepartmentListCreateView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    filterset_fields = ['faculty']
    search_fields = ['name', 'code']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]

    def get_queryset(self):
        return Department.objects.select_related('faculty').all()


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.select_related('faculty').all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class AcademicSessionListCreateView(generics.ListCreateAPIView):
    queryset = AcademicSession.objects.prefetch_related('semesters').all()
    serializer_class = AcademicSessionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class AcademicSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicSession.objects.prefetch_related('semesters').all()
    serializer_class = AcademicSessionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class SemesterListCreateView(generics.ListCreateAPIView):
    serializer_class = SemesterSerializer
    filterset_fields = ['session', 'is_current', 'is_result_published']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]

    def get_queryset(self):
        return Semester.objects.select_related('session').all()


class SemesterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semester.objects.select_related('session').all()
    serializer_class = SemesterSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class LevelListView(generics.ListAPIView):
    """GET: Anyone (AllowAny)"""
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [AllowAny]  # <-- Allows unauthenticated access


class CurrentSemesterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        semester = Semester.get_current()
        if not semester:
            return Response({'detail': 'No active semester set.'}, status=404)
        return Response(SemesterSerializer(semester).data)