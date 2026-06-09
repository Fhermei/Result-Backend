from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListCreateView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('my-courses/', views.MyCoursesView.as_view(), name='my_courses'),
    path('register/', views.RegisterCoursesView.as_view(), name='register_courses'),
    path('my-registrations/', views.MyRegisteredCoursesView.as_view(), name='my_registrations'),
    path('<int:course_id>/students/', views.CourseStudentsView.as_view(), name='course-students'),
]