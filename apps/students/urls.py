from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListCreateView.as_view(), name='student_list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('my-profile/', views.MyStudentProfileView.as_view(), name='my_profile'),
]