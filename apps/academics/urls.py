from django.urls import path
from . import views

urlpatterns = [
    path('faculties/', views.FacultyListCreateView.as_view(), name='faculty_list'),
    path('faculties/<int:pk>/', views.FacultyDetailView.as_view(), name='faculty_detail'),
    path('departments/', views.DepartmentListCreateView.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('sessions/', views.AcademicSessionListCreateView.as_view(), name='session_list'),
    path('sessions/<int:pk>/', views.AcademicSessionDetailView.as_view(), name='session_detail'),
    path('semesters/', views.SemesterListCreateView.as_view(), name='semester_list'),
    path('semesters/<int:pk>/', views.SemesterDetailView.as_view(), name='semester_detail'),
    path('current-semester/', views.CurrentSemesterView.as_view(), name='current_semester'),
    path('levels/', views.LevelListView.as_view(), name='level_list'),
]