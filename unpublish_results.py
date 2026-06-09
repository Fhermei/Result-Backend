import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.results.models import Result
from apps.academics.models import Semester

def unpublish_results_by_semester(semester_id=None, count=None, percentage=None):
    """
    Unpublish results
    - semester_id: specific semester (if None, uses current semester)
    - count: exact number of results to unpublish
    - percentage: percentage of results to unpublish (0-100)
    """
    
    # Get semester
    if semester_id:
        try:
            semester = Semester.objects.get(id=semester_id)
        except Semester.DoesNotExist:
            print(f"Semester with ID {semester_id} not found!")
            return
    else:
        semester = Semester.get_current()
        if not semester:
            print("No current semester found!")
            return
    
    print(f"Working with semester: {semester}")
    
    # Get published results for this semester
    published_results = Result.objects.filter(semester=semester, is_published=True)
    total_published = published_results.count()
    
    print(f"Total published results in {semester}: {total_published}")
    
    if total_published == 0:
        print("No published results to unpublish!")
        return
    
    # Determine how many to unpublish
    if count:
        num_to_unpublish = min(count, total_published)
    elif percentage:
        num_to_unpublish = int(total_published * percentage / 100)
    else:
        num_to_unpublish = total_published  # Default: unpublish all
    
    print(f"Will unpublish {num_to_unpublish} results...")
    
    # Get results to unpublish
    if num_to_unpublish == total_published:
        results_to_unpublish = published_results
    else:
        # Randomly select results
        result_ids = list(published_results.values_list('id', flat=True))
        selected_ids = random.sample(result_ids, num_to_unpublish)
        results_to_unpublish = Result.objects.filter(id__in=selected_ids)
    
    # Unpublish them
    updated = 0
    for result in results_to_unpublish:
        result.is_published = False
        result.blockchain_hash = None
        result.save()
        updated += 1
        if updated % 100 == 0:
            print(f"  Unpublished {updated} results...")
    
    print(f"\n✅ Successfully unpublished {updated} results!")
    
    # Show summary
    remaining_published = Result.objects.filter(semester=semester, is_published=True).count()
    print(f"\nSummary for {semester}:")
    print(f"  Previously published: {total_published}")
    print(f"  Unpublished: {updated}")
    print(f"  Now published: {remaining_published}")

def unpublish_by_course(course_code, semester_id=None):
    """Unpublish results for a specific course"""
    from apps.courses.models import Course
    
    try:
        course = Course.objects.get(code=course_code)
    except Course.DoesNotExist:
        print(f"Course {course_code} not found!")
        return
    
    if semester_id:
        semester = Semester.objects.get(id=semester_id)
    else:
        semester = Semester.get_current()
    
    results = Result.objects.filter(course=course, semester=semester, is_published=True)
    count = results.count()
    
    print(f"Found {count} published results for {course_code} in {semester}")
    
    if count == 0:
        print("No results to unpublish!")
        return
    
    confirm = input(f"Unpublish all {count} results for {course_code}? (y/n): ")
    if confirm.lower() == 'y':
        updated = results.update(is_published=False, blockchain_hash=None)
        print(f"✅ Unpublished {updated} results for {course_code}")

def unpublish_by_student(matric_no, semester_id=None):
    """Unpublish results for a specific student"""
    from apps.students.models import StudentProfile
    
    try:
        student = StudentProfile.objects.get(matric_no=matric_no)
    except StudentProfile.DoesNotExist:
        print(f"Student {matric_no} not found!")
        return
    
    if semester_id:
        semester = Semester.objects.get(id=semester_id)
    else:
        semester = Semester.get_current()
    
    results = Result.objects.filter(student=student, semester=semester, is_published=True)
    count = results.count()
    
    print(f"Found {count} published results for {student.user.get_full_name()} ({matric_no})")
    
    if count == 0:
        print("No results to unpublish!")
        return
    
    confirm = input(f"Unpublish all {count} results for this student? (y/n): ")
    if confirm.lower() == 'y':
        updated = results.update(is_published=False, blockchain_hash=None)
        print(f"✅ Unpublished {updated} results for {student.user.get_full_name()}")

def show_published_stats():
    """Show statistics of published results by semester"""
    print("\n" + "="*60)
    print("PUBLISHED RESULTS STATISTICS")
    print("="*60)
    
    for semester in Semester.objects.all():
        published = Result.objects.filter(semester=semester, is_published=True).count()
        total = Result.objects.filter(semester=semester).count()
        print(f"{semester}: {published}/{total} published ({int(published/total*100) if total > 0 else 0}%)")

def main():
    print("="*60)
    print("RESULT UNPUBLISH SCRIPT")
    print("="*60)
    
    print("\nOptions:")
    print("1. Unpublish by semester (all or random count)")
    print("2. Unpublish by course")
    print("3. Unpublish by student")
    print("4. Show published stats")
    print("5. Unpublish 500 random results")
    
    choice = input("\nEnter choice (1-5): ")
    
    if choice == '1':
        # List available semesters
        print("\nAvailable semesters:")
        for sem in Semester.objects.all():
            published = Result.objects.filter(semester=sem, is_published=True).count()
            print(f"  {sem.id}: {sem} ({published} published)")
        
        sem_id = input("\nEnter semester ID (or press Enter for current): ")
        sem_id = int(sem_id) if sem_id else None
        
        unpublish_type = input("Unpublish by (count/percentage/all): ").lower()
        if unpublish_type == 'count':
            count = int(input("How many results to unpublish: "))
            unpublish_results_by_semester(semester_id=sem_id, count=count)
        elif unpublish_type == 'percentage':
            percentage = float(input("Percentage to unpublish (0-100): "))
            unpublish_results_by_semester(semester_id=sem_id, percentage=percentage)
        else:
            unpublish_results_by_semester(semester_id=sem_id)
    
    elif choice == '2':
        course_code = input("Enter course code (e.g., CSC101): ").upper()
        unpublish_by_course(course_code)
    
    elif choice == '3':
        matric_no = input("Enter matric number: ").upper()
        unpublish_by_student(matric_no)
    
    elif choice == '4':
        show_published_stats()
    
    elif choice == '5':
        # Unpublish 500 random results
        semester = Semester.get_current()
        if not semester:
            print("No current semester found!")
            return
        
        count = 500
        print(f"\nUnpublishing {count} random published results from {semester}...")
        unpublish_results_by_semester(semester_id=semester.id, count=count)
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()