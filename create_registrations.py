import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.students.models import StudentProfile
from apps.courses.models import Course, CourseRegistration
from apps.academics.models import Semester

def create_registrations():
    print("Creating course registrations...")
    
    # Get current semester
    current_semester = Semester.get_current()
    if not current_semester:
        print("No current semester found!")
        return
    
    print(f"Current semester: {current_semester}")
    
    # Get all students (limit to first 100 for speed)
    students = StudentProfile.objects.all()[:100]
    print(f"Found {len(students)} students")
    
    # Get courses for level 100 and 200
    courses = Course.objects.filter(level__level__in=[100, 200])[:20]
    print(f"Found {len(courses)} courses")
    
    registrations_created = 0
    
    for student in students:
        # Randomly select 5-8 courses for each student
        num_courses = random.randint(5, 8)
        selected_courses = random.sample(list(courses), min(num_courses, len(courses)))
        
        for course in selected_courses:
            registration, created = CourseRegistration.objects.get_or_create(
                student=student,
                course=course,
                semester=current_semester
            )
            if created:
                registrations_created += 1
                print(f"  Registered {student.matric_no} for {course.code}")
    
    print(f"\n Created {registrations_created} course registrations!")

if __name__ == "__main__":
    create_registrations()