import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.academics.models import Department

User = get_user_model()

# Department to lecturer mapping (Nigerian university context)
DEPARTMENT_LECTURERS = {
    'Computer Science': ['Dr. Chinedu Okafor', 'Prof. Oluwaseun Adewale', 'Dr. Nkechi Eze', 'Prof. Emeka Okonkwo'],
    'Computer Engineering': ['Dr. Temitope Balogun', 'Prof. Chinonso Nwosu', 'Dr. Adeola Ogunleye'],
    'Electrical Engineering': ['Prof. Ifeanyi Chukwu', 'Dr. Oluwafemi Oladipo', 'Prof. Chinwe Nwachukwu'],
    'Accounting': ['Dr. Segun Okafor', 'Prof. Adaobi Eze', 'Dr. Okechukwu Okonkwo'],
    'Business Administration': ['Prof. Oluwadamilola Balogun', 'Dr. Chukwuma Nwosu', 'Prof. Oluwatoyin Ogunleye'],
    'Economics': ['Dr. Nneka Chukwu', 'Prof. Onyekachi Oladipo', 'Dr. Oluwafunmilayo Nwachukwu'],
    'Mass Communication': ['Prof. Chukwudi Eze', 'Dr. Oluwaseyi Okonkwo', 'Prof. Chimamanda Balogun'],
    'Law': ['Dr. Oluwole Nwosu', 'Prof. Ngozi Okafor', 'Dr. Oluwatosin Chukwu'],
}

def get_or_create_lecturer(email, first_name, last_name):
    """Get existing lecturer or create new one"""
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'role': 'lecturer',
            'is_staff': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"  Created new lecturer: {first_name} {last_name} ({email})")
    return user

def create_lecturers():
    """Create all lecturers if they don't exist"""
    lecturers = []
    
    lecturer_data = [
        # Computer Science lecturers
        {'email': 'dr.chinedu.okafor@university.edu.ng', 'first_name': 'Dr. Chinedu', 'last_name': 'Okafor', 'dept': 'Computer Science'},
        {'email': 'prof.oluwaseun.adewale@university.edu.ng', 'first_name': 'Prof. Oluwaseun', 'last_name': 'Adewale', 'dept': 'Computer Science'},
        {'email': 'dr.nkechi.eze@university.edu.ng', 'first_name': 'Dr. Nkechi', 'last_name': 'Eze', 'dept': 'Computer Science'},
        {'email': 'prof.emeka.okonkwo@university.edu.ng', 'first_name': 'Prof. Emeka', 'last_name': 'Okonkwo', 'dept': 'Computer Science'},
        
        # Computer Engineering lecturers
        {'email': 'dr.temitope.balogun@university.edu.ng', 'first_name': 'Dr. Temitope', 'last_name': 'Balogun', 'dept': 'Computer Engineering'},
        {'email': 'prof.chinonso.nwosu@university.edu.ng', 'first_name': 'Prof. Chinonso', 'last_name': 'Nwosu', 'dept': 'Computer Engineering'},
        {'email': 'dr.adeola.ogunleye@university.edu.ng', 'first_name': 'Dr. Adeola', 'last_name': 'Ogunleye', 'dept': 'Computer Engineering'},
        
        # Electrical Engineering lecturers
        {'email': 'prof.ifeanyi.chukwu@university.edu.ng', 'first_name': 'Prof. Ifeanyi', 'last_name': 'Chukwu', 'dept': 'Electrical Engineering'},
        {'email': 'dr.oluwafemi.oladipo@university.edu.ng', 'first_name': 'Dr. Oluwafemi', 'last_name': 'Oladipo', 'dept': 'Electrical Engineering'},
        {'email': 'prof.chinwe.nwachukwu@university.edu.ng', 'first_name': 'Prof. Chinwe', 'last_name': 'Nwachukwu', 'dept': 'Electrical Engineering'},
        
        # Accounting lecturers
        {'email': 'dr.segun.okafor@university.edu.ng', 'first_name': 'Dr. Segun', 'last_name': 'Okafor', 'dept': 'Accounting'},
        {'email': 'prof.adaobi.eze@university.edu.ng', 'first_name': 'Prof. Adaobi', 'last_name': 'Eze', 'dept': 'Accounting'},
        {'email': 'dr.okechukwu.okonkwo@university.edu.ng', 'first_name': 'Dr. Okechukwu', 'last_name': 'Okonkwo', 'dept': 'Accounting'},
        
        # Business Administration lecturers
        {'email': 'prof.oluwadamilola.balogun@university.edu.ng', 'first_name': 'Prof. Oluwadamilola', 'last_name': 'Balogun', 'dept': 'Business Administration'},
        {'email': 'dr.chukwuma.nwosu@university.edu.ng', 'first_name': 'Dr. Chukwuma', 'last_name': 'Nwosu', 'dept': 'Business Administration'},
        {'email': 'prof.oluwatoyin.ogunleye@university.edu.ng', 'first_name': 'Prof. Oluwatoyin', 'last_name': 'Ogunleye', 'dept': 'Business Administration'},
        
        # Economics lecturers
        {'email': 'dr.nneka.chukwu@university.edu.ng', 'first_name': 'Dr. Nneka', 'last_name': 'Chukwu', 'dept': 'Economics'},
        {'email': 'prof.onyekachi.oladipo@university.edu.ng', 'first_name': 'Prof. Onyekachi', 'last_name': 'Oladipo', 'dept': 'Economics'},
        {'email': 'dr.oluwafunmilayo.nwachukwu@university.edu.ng', 'first_name': 'Dr. Oluwafunmilayo', 'last_name': 'Nwachukwu', 'dept': 'Economics'},
        
        # Mass Communication lecturers
        {'email': 'prof.chukwudi.eze@university.edu.ng', 'first_name': 'Prof. Chukwudi', 'last_name': 'Eze', 'dept': 'Mass Communication'},
        {'email': 'dr.oluwaseyi.okonkwo@university.edu.ng', 'first_name': 'Dr. Oluwaseyi', 'last_name': 'Okonkwo', 'dept': 'Mass Communication'},
        
        # Law lecturers
        {'email': 'dr.oluwole.nwosu@university.edu.ng', 'first_name': 'Dr. Oluwole', 'last_name': 'Nwosu', 'dept': 'Law'},
        {'email': 'prof.ngozi.okafor@university.edu.ng', 'first_name': 'Prof. Ngozi', 'last_name': 'Okafor', 'dept': 'Law'},
    ]
    
    for data in lecturer_data:
        user = get_or_create_lecturer(data['email'], data['first_name'], data['last_name'])
        lecturers.append({
            'user': user,
            'dept_name': data['dept']
        })
    
    return lecturers

def assign_lecturers_to_courses(lecturers):
    """Assign lecturers to courses based on department"""
    print("\n" + "="*60)
    print("ASSIGNING LECTURERS TO COURSES")
    print("="*60)
    
    assignments = []
    
    for lecturer_info in lecturers:
        lecturer = lecturer_info['user']
        dept_name = lecturer_info['dept_name']
        
        # Get department object
        try:
            from apps.academics.models import Department
            department = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            print(f"  Department '{dept_name}' not found, skipping...")
            continue
        
        # Get courses in this department (limit to 3-5 per lecturer)
        courses = Course.objects.filter(department=department)
        
        if not courses.exists():
            print(f"  No courses found for {dept_name}, skipping...")
            continue
        
        # Assign 3-5 courses per lecturer
        num_courses = min(random.randint(3, 5), courses.count())
        assigned_courses = random.sample(list(courses), num_courses)
        
        print(f"\n  📚 {lecturer.get_full_name()} ({dept_name})")
        
        for course in assigned_courses:
            # Update course with lecturer
            course.lecturer = lecturer
            course.save()
            assignments.append({
                'lecturer': lecturer.get_full_name(),
                'course': f"{course.code} - {course.title}",
                'department': dept_name
            })
            print(f"    ✓ Assigned to: {course.code} - {course.title}")
    
    return assignments

def assign_multiple_courses_per_lecturer():
    """Assign each lecturer to 3 or more courses (alternative method)"""
    print("\n" + "="*60)
    print("ASSIGNING MULTIPLE COURSES PER LECTURER")
    print("="*60)
    
    # Get all lecturers
    lecturers = User.objects.filter(role='lecturer', is_active=True)
    
    # Get all courses
    all_courses = list(Course.objects.all())
    
    if not all_courses:
        print("No courses found in database!")
        return []
    
    assignments = []
    
    for lecturer in lecturers:
        # Assign 3-6 courses per lecturer
        num_courses = random.randint(3, 6)
        num_courses = min(num_courses, len(all_courses))
        
        assigned_courses = random.sample(all_courses, num_courses)
        
        print(f"\n  👨‍🏫 {lecturer.get_full_name()} ({lecturer.email})")
        
        for course in assigned_courses:
            # Update course with lecturer
            course.lecturer = lecturer
            course.save()
            assignments.append({
                'lecturer': lecturer.get_full_name(),
                'course': f"{course.code} - {course.title}",
                'department': course.department.name if course.department else 'N/A'
            })
            print(f"    ✓ {course.code} - {course.title}")
    
    return assignments

def show_assignment_summary(assignments):
    """Display summary of all assignments"""
    print("\n" + "="*60)
    print("ASSIGNMENT SUMMARY")
    print("="*60)
    
    # Group by lecturer
    from collections import defaultdict
    lecturer_courses = defaultdict(list)
    
    for assignment in assignments:
        lecturer_courses[assignment['lecturer']].append(assignment['course'])
    
    for lecturer, courses in lecturer_courses.items():
        print(f"\n📖 {lecturer}")
        print(f"   Courses ({len(courses)}):")
        for course in courses:
            print(f"     - {course}")
    
    print(f"\n✅ Total assignments: {len(assignments)}")
    print(f"✅ Lecturers assigned: {len(lecturer_courses)}")

def clear_existing_assignments():
    """Clear all existing lecturer assignments from courses"""
    print("\n" + "="*60)
    print("CLEARING EXISTING ASSIGNMENTS")
    print("="*60)
    
    # Get count of courses with lecturers
    courses_with_lecturers = Course.objects.filter(lecturer__isnull=False)
    count = courses_with_lecturers.count()
    
    if count > 0:
        confirm = input(f"Found {count} courses with existing lecturer assignments. Clear them? (y/n): ")
        if confirm.lower() == 'y':
            Course.objects.all().update(lecturer=None)
            print(f"✅ Cleared {count} existing assignments")
        else:
            print("Keeping existing assignments")
    else:
        print("No existing assignments found")

def main():
    print("="*60)
    print("🎓 LECTURER TO COURSE ASSIGNMENT SCRIPT")
    print("="*60)
    
    # First, check if we have courses
    course_count = Course.objects.count()
    lecturer_count = User.objects.filter(role='lecturer').count()
    
    print(f"\n📊 Current Database Status:")
    print(f"   Total Courses: {course_count}")
    print(f"   Total Lecturers: {lecturer_count}")
    
    if course_count == 0:
        print("\n❌ No courses found! Please run populate_db.py first.")
        return
    
    # Option to clear existing assignments
    clear_existing_assignments()
    
    # Option 1: Create lecturers and assign by department
    print("\n📝 Creating/Updating lecturers...")
    lecturers = create_lecturers()
    print(f"✅ Total lecturers available: {len(lecturers)}")
    
    # Assign lecturers to courses by department
    assignments = assign_lecturers_to_courses(lecturers)
    
    # If not enough assignments, try the alternative method
    if len(assignments) < 20:
        print("\n⚠️ Not enough assignments. Trying alternative method...")
        more_assignments = assign_multiple_courses_per_lecturer()
        assignments.extend(more_assignments)
    
    # Show summary
    show_assignment_summary(assignments)
    
    # Verify assignments
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    assigned_courses = Course.objects.filter(lecturer__isnull=False)
    unassigned_courses = Course.objects.filter(lecturer__isnull=True)
    
    print(f"\n Courses with assigned lecturers: {assigned_courses.count()}")
    print(f"  Courses without lecturers: {unassigned_courses.count()}")
    
    # Show sample of assigned courses
    if assigned_courses.exists():
        print("\n Sample of assigned courses:")
        for course in assigned_courses[:10]:
            print(f"   {course.code} - {course.title} → {course.lecturer.get_full_name()}")

if __name__ == "__main__":
    main()