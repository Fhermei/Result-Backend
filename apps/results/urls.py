from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResultListCreateView.as_view(), name='result_list'),
    path('<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
    path('bulk-upload/', views.BulkResultUploadView.as_view(), name='bulk_upload'),
    path('my-results/', views.MyResultsView.as_view(), name='my_results'),
    path('gpa/', views.SemesterGPAView.as_view(), name='gpa_list'),
    path('calculate-gpa/', views.CalculateGPAView.as_view(), name='calculate_gpa'),
    path('calculate-cgpa/', views.CalculateCGPAView.as_view(), name='calculate_cgpa'),
    path('publish/', views.PublishResultsView.as_view(), name='publish_results'),
    path('transcript/<int:student_id>/', views.TranscriptView.as_view(), name='transcript'),
    path('transcript/', views.TranscriptView.as_view(), name='my_transcript'),
]