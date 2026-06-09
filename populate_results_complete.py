import os
import django
import random
from datetime import datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import models
from apps.academics.models import Faculty, Department, AcademicSession, Semester, Level
from apps.courses.models import Course, CourseRegistration
from apps.students.models import StudentProfile
from apps.results.models import Result, SemesterGPARecord, CGPARecord

User = get_user_model()

# Grade calculation functions
GRADE_POINTS = {
    'A': 5.0,
    'B': 4.0,
    'C': 3.0,
    'D': 2.0,
    'E': 1.0,
    'F': 0.0,
}

def calculate_grade(score):
    if score >= 70: return 'A'
    elif score >= 60: return 'B'
    elif score >= 50: return 'C'
    elif score >= 45: return 'D'
    elif score >= 40: return 'E'
    else: return 'F'

def calculate_gpa(results_data):
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
    total_quality_points_all = sum(s['total_quality_points'] for s in semester_data)
    total_credit_units_all = sum(s['total_credit_units'] for s in semester_data)
    if total_credit_units_all == 0:
        return 0.0
    cgpa = total_quality_points_all / total_credit_units_all
    return round(cgpa, 2)

def get_class_degree(cgpa):
    if cgpa >= 4.50: return 'First Class'
    elif cgpa >= 3.50: return 'Second Class Upper'
    elif cgpa >= 2.40: return 'Second Class Lower'
    elif cgpa >= 1.50: return 'Third Class'
    elif cgpa >= 1.00: return 'Pass'
    else: return 'Probation'

# GST Courses
GST_COURSES = [
    {'code': 'GST101', 'title': 'Use of English', 'unit': 2, 'level': 100},
    {'code': 'GST102', 'title': 'Nigerian Peoples and Culture', 'unit': 2, 'level': 100},
    {'code': 'GST103', 'title': 'Logic and Philosophy', 'unit': 2, 'level': 100},
    {'code': 'GST201', 'title': 'Entrepreneurship', 'unit': 2, 'level': 200},
    {'code': 'GST202', 'title': 'Peace and Conflict Resolution', 'unit': 2, 'level': 200},
]

# Department specific courses
DEPARTMENT_COURSES = {
    'Computer Engineering': [
        {'code': 'CEN101', 'title': 'Computer Engineering Fundamentals', 'unit': 3, 'level': 100},
        {'code': 'CEN102', 'title': 'Digital Logic Design', 'unit': 3, 'level': 100},
        {'code': 'CEN103', 'title': 'Programming in C', 'unit': 3, 'level': 100},
        {'code': 'CEN201', 'title': 'Microprocessors', 'unit': 3, 'level': 200},
        {'code': 'CEN202', 'title': 'Computer Architecture', 'unit': 3, 'level': 200},
        {'code': 'CEN203', 'title': 'Data Structures', 'unit': 3, 'level': 200},
        {'code': 'CEN301', 'title': 'Embedded Systems', 'unit': 3, 'level': 300},
        {'code': 'CEN302', 'title': 'Computer Networks', 'unit': 3, 'level': 300},
        {'code': 'CEN303', 'title': 'Operating Systems', 'unit': 3, 'level': 300},
        {'code': 'CEN401', 'title': 'VLSI Design', 'unit': 3, 'level': 400},
        {'code': 'CEN402', 'title': 'Robotics', 'unit': 3, 'level': 400},
        {'code': 'CEN403', 'title': 'Project', 'unit': 6, 'level': 400},
    ],
    'Computer Science': [
        {'code': 'CSC101', 'title': 'Introduction to Computer Science', 'unit': 3, 'level': 100},
        {'code': 'CSC102', 'title': 'Programming in C', 'unit': 3, 'level': 100},
        {'code': 'CSC103', 'title': 'Discrete Mathematics', 'unit': 3, 'level': 100},
        {'code': 'CSC201', 'title': 'Data Structures', 'unit': 3, 'level': 200},
        {'code': 'CSC202', 'title': 'Object Oriented Programming', 'unit': 3, 'level': 200},
        {'code': 'CSC203', 'title': 'Database Management Systems', 'unit': 3, 'level': 200},
        {'code': 'CSC204', 'title': 'Operating Systems', 'unit': 3, 'level': 200},
        {'code': 'CSC301', 'title': 'Software Engineering', 'unit': 3, 'level': 300},
        {'code': 'CSC302', 'title': 'Computer Networks', 'unit': 3, 'level': 300},
        {'code': 'CSC303', 'title': 'Web Development', 'unit': 3, 'level': 300},
        {'code': 'CSC304', 'title': 'Artificial Intelligence', 'unit': 3, 'level': 300},
        {'code': 'CSC401', 'title': 'Project Management', 'unit': 2, 'level': 400},
        {'code': 'CSC402', 'title': 'Cyber Security', 'unit': 3, 'level': 400},
        {'code': 'CSC403', 'title': 'Final Year Project', 'unit': 6, 'level': 400},
    ],
    'Electrical Engineering': [
        {'code': 'EEN101', 'title': 'Electrical Engineering Fundamentals', 'unit': 3, 'level': 100},
        {'code': 'EEN102', 'title': 'Circuit Theory I', 'unit': 3, 'level': 100},
        {'code': 'EEN201', 'title': 'Circuit Theory II', 'unit': 3, 'level': 200},
        {'code': 'EEN202', 'title': 'Electronics I', 'unit': 3, 'level': 200},
        {'code': 'EEN203', 'title': 'Electrical Machines', 'unit': 3, 'level': 200},
        {'code': 'EEN301', 'title': 'Power Systems', 'unit': 3, 'level': 300},
        {'code': 'EEN302', 'title': 'Control Systems', 'unit': 3, 'level': 300},
        {'code': 'EEN303', 'title': 'Digital Signal Processing', 'unit': 3, 'level': 300},
        {'code': 'EEN401', 'title': 'Power Electronics', 'unit': 3, 'level': 400},
        {'code': 'EEN402', 'title': 'Project', 'unit': 6, 'level': 400},
    ],
    'Mechanical Engineering': [
        {'code': 'MEE101', 'title': 'Introduction to Mechanical Engineering', 'unit': 3, 'level': 100},
        {'code': 'MEE102', 'title': 'Engineering Mechanics', 'unit': 3, 'level': 100},
        {'code': 'MEE103', 'title': 'Workshop Technology', 'unit': 2, 'level': 100},
        {'code': 'MEE201', 'title': 'Thermodynamics I', 'unit': 3, 'level': 200},
        {'code': 'MEE202', 'title': 'Fluid Mechanics', 'unit': 3, 'level': 200},
        {'code': 'MEE203', 'title': 'Strength of Materials', 'unit': 3, 'level': 200},
        {'code': 'MEE204', 'title': 'Engineering Drawing', 'unit': 2, 'level': 200},
        {'code': 'MEE301', 'title': 'Heat Transfer', 'unit': 3, 'level': 300},
        {'code': 'MEE302', 'title': 'Machine Design', 'unit': 3, 'level': 300},
        {'code': 'MEE303', 'title': 'Thermodynamics II', 'unit': 3, 'level': 300},
        {'code': 'MEE401', 'title': 'Internal Combustion Engines', 'unit': 3, 'level': 400},
        {'code': 'MEE402', 'title': 'Refrigeration', 'unit': 3, 'level': 400},
        {'code': 'MEE403', 'title': 'Project', 'unit': 6, 'level': 400},
    ],
    'Chemical Engineering': [
        {'code': 'CHE101', 'title': 'Introduction to Chemical Engineering', 'unit': 3, 'level': 100},
        {'code': 'CHE102', 'title': 'General Chemistry', 'unit': 3, 'level': 100},
        {'code': 'CHE201', 'title': 'Chemical Process Principles', 'unit': 3, 'level': 200},
        {'code': 'CHE202', 'title': 'Fluid Flow Operations', 'unit': 3, 'level': 200},
        {'code': 'CHE203', 'title': 'Chemical Engineering Thermodynamics', 'unit': 3, 'level': 200},
        {'code': 'CHE301', 'title': 'Heat Transfer Operations', 'unit': 3, 'level': 300},
        {'code': 'CHE302', 'title': 'Mass Transfer Operations', 'unit': 3, 'level': 300},
        {'code': 'CHE303', 'title': 'Chemical Reaction Engineering', 'unit': 3, 'level': 300},
        {'code': 'CHE401', 'title': 'Process Design', 'unit': 3, 'level': 400},
        {'code': 'CHE402', 'title': 'Plant Economics', 'unit': 3, 'level': 400},
        {'code': 'CHE403', 'title': 'Project', 'unit': 6, 'level': 400},
    ],
    'Accounting': [
        {'code': 'ACC101', 'title': 'Introduction to Accounting', 'unit': 3, 'level': 100},
        {'code': 'ACC102', 'title': 'Financial Accounting I', 'unit': 3, 'level': 100},
        {'code': 'ACC201', 'title': 'Financial Accounting II', 'unit': 3, 'level': 200},
        {'code': 'ACC202', 'title': 'Cost Accounting', 'unit': 3, 'level': 200},
        {'code': 'ACC301', 'title': 'Management Accounting', 'unit': 3, 'level': 300},
        {'code': 'ACC302', 'title': 'Taxation', 'unit': 3, 'level': 300},
        {'code': 'ACC401', 'title': 'Auditing', 'unit': 3, 'level': 400},
        {'code': 'ACC402', 'title': 'Financial Reporting', 'unit': 3, 'level': 400},
    ],
    'Economics': [
        {'code': 'ECO101', 'title': 'Principles of Economics I', 'unit': 3, 'level': 100},
        {'code': 'ECO102', 'title': 'Principles of Economics II', 'unit': 3, 'level': 100},
        {'code': 'ECO201', 'title': 'Microeconomic Theory', 'unit': 3, 'level': 200},
        {'code': 'ECO202', 'title': 'Macroeconomic Theory', 'unit': 3, 'level': 200},
        {'code': 'ECO301', 'title': 'Econometrics', 'unit': 3, 'level': 300},
        {'code': 'ECO302', 'title': 'Development Economics', 'unit': 3, 'level': 300},
        {'code': 'ECO401', 'title': 'International Economics', 'unit': 3, 'level': 400},
        {'code': 'ECO402', 'title': 'Project', 'unit': 6, 'level': 400},
    ],
}

def create_courses():
    """Create courses for all departments"""
    print("Creating courses...")
    courses_created = 0
    
    # Get or create default session and semester
    default_session, _ = AcademicSession.objects.get_or_create(
        name='2024/2025',
        defaults={'start_date': '2024-09-01', 'end_date': '2025-07-31', 'is_current': True}
    )
    default_semester, _ = Semester.objects.get_or_create(
        session=default_session,
        name='first',
        defaults={'is_current': True}
    )
    
    # Create department-specific courses
    for dept_name, courses_data in DEPARTMENT_COURSES.items():
        try:
            department = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            print(f"  Department {dept_name} not found, skipping...")
            continue
        
        for course_data in courses_data:
            try:
                level = Level.objects.get(level=course_data['level'])
                
                course, created = Course.objects.get_or_create(
                    code=course_data['code'],
                    department=department,
                    defaults={
                        'title': course_data['title'],
                        'credit_unit': course_data['unit'],
                        'level': level,
                        'semester': default_semester,
                        'is_elective': False
                    }
                )
                if created:
                    courses_created += 1
                    print(f"    Created: {course.code} - {course.title}")
            except Exception as e:
                print(f"    Error creating {course_data['code']}: {e}")
    
    # Create GST courses for all departments
    for dept in Department.objects.all():
        for gst_data in GST_COURSES:
            try:
                level = Level.objects.get(level=gst_data['level'])
                course, created = Course.objects.get_or_create(
                    code=gst_data['code'],
                    department=dept,
                    defaults={
                        'title': gst_data['title'],
                        'credit_unit': gst_data['unit'],
                        'level': level,
                        'semester': default_semester,
                        'is_elective': False
                    }
                )
                if created:
                    courses_created += 1
            except Exception as e:
                pass
    
    print(f"  Total new courses created: {courses_created}")
    return courses_created

def get_courses_for_student(student, semester, expected_level):
    """Get courses appropriate for a student based on their level and department"""
    department = student.department
    
    try:
        level_obj = Level.objects.get(level=expected_level)
    except Level.DoesNotExist:
        return []
    
    # Get courses for this department at this level
    courses = list(Course.objects.filter(
        department=department,
        level=level_obj
    ))
    
    # Add GST courses
    gst_courses = list(Course.objects.filter(
        code__startswith='GST',
        level=level_obj
    ))
    courses.extend(gst_courses)
    
    # Remove duplicates
    courses = list({c.id: c for c in courses}.values())
    
    return courses

def generate_random_score():
    """Generate realistic random score"""
    if random.random() < 0.7:
        return random.randint(45, 75)
    elif random.random() < 0.85:
        return random.randint(75, 100)
    else:
        return random.randint(20, 44)

def create_results_for_student(student, semesters):
    """Create results for a student across multiple semesters"""
    print(f"  Processing: {student.matric_no} - {student.user.get_full_name()}")
    print(f"    Department: {student.department.name}")
    print(f"    Current Level: {student.current_level.level}")
    
    semester_data = []
    total_results_created = 0
    
    for semester in semesters:
        # Determine appropriate level for this semester
        session_year = int(semester.session.name.split('/')[0])
        admission_year = student.admission_year
        years_elapsed = session_year - admission_year
        
        if years_elapsed < 0:
            continue
        
        # Calculate expected level
        if years_elapsed == 0:
            expected_level = 100
        else:
            expected_level = 100 + (years_elapsed * 100)
        
        # Skip if level is beyond student's current or beyond 500
        if expected_level > 500:
            continue
        
        # Get courses for this level
        courses = get_courses_for_student(student, semester, expected_level)
        
        if not courses:
            continue
        
        # Select 5-8 random courses
        num_courses = min(random.randint(5, 8), len(courses))
        selected_courses = random.sample(courses, num_courses)
        
        # Create results for each course
        results_data = []
        
        for course in selected_courses:
            ca_score = random.randint(20, 40)
            exam_score = random.randint(20, 70)
            total_score = ca_score + exam_score
            grade = calculate_grade(total_score)
            
            result, created = Result.objects.update_or_create(
                student=student,
                course=course,
                semester=semester,
                defaults={
                    'ca_score': ca_score,
                    'exam_score': exam_score,
                    'is_published': True,
                    'published_at': datetime.now()
                }
            )
            
            if created:
                total_results_created += 1
            
            results_data.append({
                'credit_unit': course.credit_unit,
                'grade': grade
            })
        
        # Calculate GPA
        if results_data:
            gpa, total_qp, total_cu = calculate_gpa(results_data)
            class_degree = get_class_degree(gpa)
            
            SemesterGPARecord.objects.update_or_create(
                student=student,
                semester=semester,
                defaults={
                    'gpa': gpa,
                    'total_quality_points': total_qp,
                    'total_credit_units': total_cu,
                    'class_degree': class_degree
                }
            )
            
            semester_data.append({
                'total_quality_points': total_qp,
                'total_credit_units': total_cu
            })
            
            print(f"      {semester.session.name} - {semester.name}: GPA = {gpa}, Courses = {len(results_data)}")
    
    # Calculate CGPA
    if semester_data:
        cgpa = calculate_cgpa(semester_data)
        class_degree = get_class_degree(cgpa)
        total_qp = sum(s['total_quality_points'] for s in semester_data)
        total_cu = sum(s['total_credit_units'] for s in semester_data)
        
        CGPARecord.objects.update_or_create(
            student=student,
            defaults={
                'cgpa': cgpa,
                'total_quality_points_all': total_qp,
                'total_credit_units_all': total_cu,
                'class_degree': class_degree
            }
        )
        
        print(f"    FINAL CGPA: {cgpa} - {class_degree}")
    
    return len(semester_data), total_results_created

def get_semesters_for_student(student):
    """Get all relevant semesters for a student"""
    admission_year = student.admission_year
    current_year = 2025
    max_year = min(current_year, admission_year + 6)
    
    semesters = []
    
    for year in range(admission_year, max_year + 1):
        session_name = f"{year}/{year + 1}"
        try:
            session = AcademicSession.objects.get(name=session_name)
        except AcademicSession.DoesNotExist:
            continue
        
        for sem_name in ['first', 'second']:
            try:
                semester = Semester.objects.get(session=session, name=sem_name)
                semesters.append(semester)
            except Semester.DoesNotExist:
                continue
    
    return semesters

def populate_all_results():
    """Main function to populate results for all students"""
    print("=" * 70)
    print("COMPLETE RESULT POPULATION SYSTEM")
    print("=" * 70)
    
    # Step 1: Create courses
    print("\n[STEP 1] Creating courses...")
    create_courses()
    
    # Step 2: Get all students
    print("\n[STEP 2] Loading students...")
    students = StudentProfile.objects.all()
    print(f"  Total students found: {students.count()}")
    
    # Step 3: Clear existing results
    print("\n[STEP 3] Clearing existing results...")
    confirm = input("  Clear all existing results before populating? (y/n): ")
    if confirm.lower() == 'y':
        Result.objects.all().delete()
        SemesterGPARecord.objects.all().delete()
        CGPARecord.objects.all().delete()
        print("  Existing results cleared.")
    else:
        print("  Keeping existing results.")
    
    # Step 4: Process each student
    print("\n[STEP 4] Creating results for students...")
    print("-" * 50)
    
    total_students_processed = 0
    total_semesters_processed = 0
    total_results_created = 0
    
    for idx, student in enumerate(students):
        print(f"\n[{idx + 1}/{students.count()}] {student.matric_no}")
        
        semesters = get_semesters_for_student(student)
        
        if not semesters:
            print(f"    No semesters found")
            continue
        
        semesters_count, results_count = create_results_for_student(student, semesters)
        total_semesters_processed += semesters_count
        total_results_created += results_count
        total_students_processed += 1
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("POPULATION COMPLETE")
    print("=" * 70)
    print(f"  Students processed: {total_students_processed}")
    print(f"  Semesters processed: {total_semesters_processed}")
    print(f"  Results created: {total_results_created}")
    print(f"  Total results in database: {Result.objects.count()}")
    print(f"  GPA records: {SemesterGPARecord.objects.count()}")
    print(f"  CGPA records: {CGPARecord.objects.count()}")
    print("=" * 70)

if __name__ == "__main__":
    populate_all_results()