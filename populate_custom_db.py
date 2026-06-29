import os
import django
import random
import sys
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from apps.academics.models import Faculty, Department, AcademicSession, Semester, Level
from apps.courses.models import Course, CourseRegistration
from apps.students.models import StudentProfile
from apps.results.models import Result, SemesterGPARecord, CGPARecord

User = get_user_model()

# ============================================================
# CONFIGURATION
# ============================================================
NUM_STUDENTS = 122
NUM_LECTURERS = 20
NUM_ADMINS = 3
PASSWORD = 'admin123'
NON_INTERACTIVE = '--non-interactive' in sys.argv
if NON_INTERACTIVE:
    sys.argv.remove('--non-interactive')

# ============================================================
# NIGERIAN NAMES
# ============================================================
NIGERIAN_FIRST_NAMES = [
    'Chinedu', 'Olufemi', 'Adebayo', 'Ngozi', 'Chiamaka', 'Oluwaseun', 'Ifeanyi',
    'Temitope', 'Chukwudi', 'Funmilayo', 'Emeka', 'Blessing', 'Olayinka', 'Chinonso',
    'Segun', 'Adaeze', 'Obinna', 'Similoluwa', 'Oluwatobi', 'Chidimma', 'Ayomide',
    'Chibueze', 'Oluwafemi', 'Chisom', 'Oluwaseyi', 'Chukwuemeka', 'Tolulope',
    'Nneka', 'Okechukwu', 'Ifeoluwa', 'Oluwadamilola', 'Chukwuma', 'Oluwatoyin',
    'Adanna', 'Onyekachi', 'Oluwafunmilayo', 'Chinemerem', 'Oluwaseun', 'Chukwudi'
]

NIGERIAN_LAST_NAMES = [
    'Okafor', 'Adewale', 'Ogunleye', 'Eze', 'Okonkwo', 'Balogun', 'Nwosu',
    'Adebayo', 'Onyeka', 'Oladipo', 'Chukwu', 'Oluwole', 'Nwachukwu', 'Oyedele',
    'Okeke', 'Ogunbiyi', 'Nwankwo', 'Ogunyemi', 'Ekwueme', 'Ogunlana', 'Nweke',
    'Ogunwale', 'Okpara', 'Ogunjobi', 'Nwagwu', 'Ogunlade', 'Okoro', 'Ogunmuyiwa'
]

# ============================================================
# FACULTIES AND DEPARTMENTS
# ============================================================
FACULTIES_DATA = [
    {
        'name': 'Faculty of Engineering',
        'code': 'ENG',
        'departments': [
            {'name': 'Computer Engineering', 'code': 'CEN'},
            {'name': 'Electrical Engineering', 'code': 'EEN'},
            {'name': 'Mechanical Engineering', 'code': 'MEN'},
            {'name': 'Civil Engineering', 'code': 'CIV'},
            {'name': 'Chemical Engineering', 'code': 'CHE'},
        ]
    },
    {
        'name': 'Faculty of Science',
        'code': 'SCI',
        'departments': [
            {'name': 'Computer Science', 'code': 'CSC'},
            {'name': 'Mathematics', 'code': 'MAT'},
            {'name': 'Physics', 'code': 'PHY'},
            {'name': 'Chemistry', 'code': 'CHM'},
            {'name': 'Biochemistry', 'code': 'BCH'},
        ]
    },
    {
        'name': 'Faculty of Social Sciences',
        'code': 'SOC',
        'departments': [
            {'name': 'Economics', 'code': 'ECO'},
            {'name': 'Political Science', 'code': 'POL'},
            {'name': 'Sociology', 'code': 'SOC'},
            {'name': 'Psychology', 'code': 'PSY'},
            {'name': 'Mass Communication', 'code': 'MAC'},
        ]
    },
    {
        'name': 'Faculty of Arts',
        'code': 'ART',
        'departments': [
            {'name': 'English Language', 'code': 'ENG'},
            {'name': 'History', 'code': 'HIS'},
            {'name': 'Philosophy', 'code': 'PHI'},
            {'name': 'Linguistics', 'code': 'LIN'},
        ]
    },
    {
        'name': 'Faculty of Management Sciences',
        'code': 'MGT',
        'departments': [
            {'name': 'Business Administration', 'code': 'BUS'},
            {'name': 'Accounting', 'code': 'ACC'},
            {'name': 'Banking and Finance', 'code': 'BNF'},
            {'name': 'Marketing', 'code': 'MKT'},
        ]
    },
    {
        'name': 'Faculty of Law',
        'code': 'LAW',
        'departments': [
            {'name': 'Law', 'code': 'LAW'},
        ]
    },
]

# ============================================================
# COURSES DATA
# ============================================================
COURSES_DATA = {
    'CSC': [
        {'code': 'CSC101', 'title': 'Introduction to Computer Science', 'unit': 3, 'level': 100},
        {'code': 'CSC102', 'title': 'Programming in C', 'unit': 3, 'level': 100},
        {'code': 'CSC201', 'title': 'Data Structures', 'unit': 3, 'level': 200},
        {'code': 'CSC202', 'title': 'Object Oriented Programming', 'unit': 3, 'level': 200},
        {'code': 'CSC203', 'title': 'Database Management Systems', 'unit': 3, 'level': 200},
        {'code': 'CSC204', 'title': 'Operating Systems', 'unit': 3, 'level': 200},
        {'code': 'CSC301', 'title': 'Software Engineering', 'unit': 3, 'level': 300},
        {'code': 'CSC302', 'title': 'Computer Networks', 'unit': 3, 'level': 300},
        {'code': 'CSC303', 'title': 'Web Development', 'unit': 3, 'level': 300},
        {'code': 'CSC401', 'title': 'Artificial Intelligence', 'unit': 3, 'level': 400},
        {'code': 'CSC402', 'title': 'Project Management', 'unit': 2, 'level': 400},
        {'code': 'CSC403', 'title': 'Final Year Project', 'unit': 6, 'level': 400},
    ],
    'CEN': [
        {'code': 'CEN101', 'title': 'Computer Engineering Fundamentals', 'unit': 3, 'level': 100},
        {'code': 'CEN102', 'title': 'Digital Logic Design', 'unit': 3, 'level': 100},
        {'code': 'CEN201', 'title': 'Microprocessors', 'unit': 3, 'level': 200},
        {'code': 'CEN202', 'title': 'Computer Architecture', 'unit': 3, 'level': 200},
        {'code': 'CEN301', 'title': 'Embedded Systems', 'unit': 3, 'level': 300},
    ],
    'ECO': [
        {'code': 'ECO101', 'title': 'Principles of Economics I', 'unit': 3, 'level': 100},
        {'code': 'ECO102', 'title': 'Principles of Economics II', 'unit': 3, 'level': 100},
        {'code': 'ECO201', 'title': 'Microeconomic Theory', 'unit': 3, 'level': 200},
        {'code': 'ECO202', 'title': 'Macroeconomic Theory', 'unit': 3, 'level': 200},
        {'code': 'ECO301', 'title': 'Econometrics', 'unit': 3, 'level': 300},
    ],
    'ACC': [
        {'code': 'ACC101', 'title': 'Introduction to Accounting', 'unit': 3, 'level': 100},
        {'code': 'ACC102', 'title': 'Financial Accounting I', 'unit': 3, 'level': 100},
        {'code': 'ACC201', 'title': 'Financial Accounting II', 'unit': 3, 'level': 200},
        {'code': 'ACC202', 'title': 'Cost Accounting', 'unit': 3, 'level': 200},
        {'code': 'ACC301', 'title': 'Management Accounting', 'unit': 3, 'level': 300},
    ],
    'BUS': [
        {'code': 'BUS101', 'title': 'Introduction to Business', 'unit': 3, 'level': 100},
        {'code': 'BUS102', 'title': 'Principles of Management', 'unit': 3, 'level': 100},
        {'code': 'BUS201', 'title': 'Organizational Behaviour', 'unit': 3, 'level': 200},
        {'code': 'BUS202', 'title': 'Business Communication', 'unit': 2, 'level': 200},
    ],
    'LAW': [
        {'code': 'LAW101', 'title': 'Nigerian Legal System', 'unit': 3, 'level': 100},
        {'code': 'LAW102', 'title': 'Law of Contract', 'unit': 3, 'level': 100},
        {'code': 'LAW201', 'title': 'Constitutional Law', 'unit': 3, 'level': 200},
        {'code': 'LAW202', 'title': 'Criminal Law', 'unit': 3, 'level': 200},
    ],
}

# ============================================================
# GPA FUNCTIONS
# ============================================================
GRADE_POINTS = {'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0}

def calculate_grade(score):
    if score >= 70: return 'A'
    elif score >= 60: return 'B'
    elif score >= 50: return 'C'
    elif score >= 45: return 'D'
    elif score >= 40: return 'E'
    else: return 'F'

def calculate_gpa(results_data):
    total_qp = 0
    total_cu = 0
    for r in results_data:
        total_qp += r['credit_unit'] * GRADE_POINTS.get(r['grade'], 0)
        total_cu += r['credit_unit']
    if total_cu == 0:
        return 0.0, 0, 0
    return round(total_qp / total_cu, 2), total_qp, total_cu

def calculate_cgpa(semester_data):
    total_qp = sum(s['total_quality_points'] for s in semester_data)
    total_cu = sum(s['total_credit_units'] for s in semester_data)
    if total_cu == 0:
        return 0.0
    return round(total_qp / total_cu, 2)

def get_class_degree(cgpa):
    if cgpa >= 4.50: return 'First Class'
    elif cgpa >= 3.50: return 'Second Class Upper'
    elif cgpa >= 2.40: return 'Second Class Lower'
    elif cgpa >= 1.50: return 'Third Class'
    elif cgpa >= 1.00: return 'Pass'
    else: return 'Probation'

# ============================================================
# POPULATION FUNCTIONS
# ============================================================
def create_faculties_and_departments():
    print("Creating Faculties and Departments...")
    faculties = {}
    departments = {}
    for faculty_data in FACULTIES_DATA:
        faculty, _ = Faculty.objects.get_or_create(
            code=faculty_data['code'],
            defaults={'name': faculty_data['name']}
        )
        faculties[faculty_data['code']] = faculty
        for dept_data in faculty_data['departments']:
            dept, _ = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name'], 'faculty': faculty}
            )
            departments[dept_data['code']] = dept
            print(f"  Created: {faculty.name} -> {dept.name}")
    return faculties, departments

def create_levels():
    print("\nCreating Levels...")
    levels = {}
    for level_value in [100, 200, 300, 400, 500]:
        level, _ = Level.objects.get_or_create(level=level_value)
        levels[level_value] = level
        print(f"  Created: {level_value} Level")
    return levels

def create_academic_sessions():
    print("\nCreating Academic Sessions...")
    sessions = {}
    sessions_data = [
        {'name': '2020/2021', 'start': '2020-09-01', 'end': '2021-07-31'},
        {'name': '2021/2022', 'start': '2021-09-01', 'end': '2022-07-31'},
        {'name': '2022/2023', 'start': '2022-09-01', 'end': '2023-07-31'},
        {'name': '2023/2024', 'start': '2023-09-01', 'end': '2024-07-31'},
        {'name': '2024/2025', 'start': '2024-09-01', 'end': '2025-07-31'},
        {'name': '2025/2026', 'start': '2025-09-01', 'end': '2026-07-31', 'is_current': True},
    ]
    for sd in sessions_data:
        session, _ = AcademicSession.objects.get_or_create(
            name=sd['name'],
            defaults={
                'start_date': sd['start'],
                'end_date': sd['end'],
                'is_current': sd.get('is_current', False)
            }
        )
        sessions[sd['name']] = session
        print(f"  Created: {session.name}")
    return sessions

def create_semesters(sessions):
    print("\nCreating Semesters...")
    semesters = {}
    for session_name, session in sessions.items():
        for sem_name, sem_display in [('first', 'First Semester'), ('second', 'Second Semester')]:
            is_current = (session_name == '2025/2026' and sem_name == 'first')
            semester, _ = Semester.objects.get_or_create(
                session=session,
                name=sem_name,
                defaults={'is_current': is_current}
            )
            semesters[f"{session_name}_{sem_name}"] = semester
            print(f"  Created: {session.name} - {sem_display}")
    return semesters

def create_super_admin():
    print("\nCreating Super Admin...")
    user, created = User.objects.get_or_create(
        email='admin@gmail.com',
        defaults={
            'first_name': 'Super',
            'last_name': 'Admin',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        user.set_password(PASSWORD)
        user.save()
        print(f"  Created Super Admin: admin@gmail.com")
    else:
        print(f"  Super Admin already exists")
    return user

def create_admin_users():
    print("\nCreating School Admins...")
    admins = []
    admin_data = [
        ('Dr. Chiamaka', 'Eze'),
        ('Dr. Olufemi', 'Adewale'),
        ('Dr. Funmilayo', 'Balogun'),
    ]
    for i, (first_name, last_name) in enumerate(admin_data):
        email = f"{first_name.lower().replace(' ', '').replace('.', '')}.{last_name.lower()}{random.randint(10, 99)}@gmail.com"
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': 'admin',
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            user.set_password(PASSWORD)
            user.save()
            admins.append(user)
            print(f"  Created Admin: {first_name} {last_name} ({email})")
    return admins

def create_lecturer_users():
    print(f"\nCreating {NUM_LECTURERS} Lecturer Users...")
    lecturers = []
    for i in range(NUM_LECTURERS):
        first_name = random.choice(NIGERIAN_FIRST_NAMES)
        last_name = random.choice(NIGERIAN_LAST_NAMES)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@gmail.com"
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': 'lecturer',
                'is_staff': True,
            }
        )
        if created:
            user.set_password(PASSWORD)
            user.save()
            lecturers.append(user)
            print(f"  Created Lecturer {i+1}: {first_name} {last_name} ({email})")
    return lecturers

def create_students(departments, levels):
    print(f"\nCreating {NUM_STUDENTS} Student Users...")
    students = []
    admission_years = [2020, 2021, 2022, 2023, 2024, 2025]
    departments_list = list(departments.values())
    
    for i in range(NUM_STUDENTS):
        first_name = random.choice(NIGERIAN_FIRST_NAMES)
        last_name = random.choice(NIGERIAN_LAST_NAMES)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@gmail.com"
        matric_no = f"U{random.randint(20, 25)}/{random.choice(['01', '02', '03', '04', '05'])}/{str(i+1000).zfill(4)}"
        admission_year = random.choice(admission_years)
        
        current_year = 2025
        years_elapsed = current_year - admission_year
        if years_elapsed >= 4: level_value = 400
        elif years_elapsed == 3: level_value = 300
        elif years_elapsed == 2: level_value = 200
        elif years_elapsed == 1: level_value = 100
        else: level_value = 100
        
        level = levels.get(level_value, levels[100])
        department = random.choice(departments_list)
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': 'student',
            }
        )
        if created:
            user.set_password(PASSWORD)
            user.save()
            student, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'matric_no': matric_no,
                    'department': department,
                    'current_level': level,
                    'admission_year': admission_year,
                }
            )
            students.append(student)
            if (i + 1) % 20 == 0:
                print(f"  Created {i + 1} students...")
    
    print(f"  Successfully created {len(students)} students")
    return students

def create_courses(departments, levels, semesters):
    print("\nCreating Courses...")
    courses = {}
    first_semester_2025 = semesters.get('2025/2026_first')
    second_semester_2025 = semesters.get('2025/2026_second')
    
    # Create GST courses ONCE (not for each department)
    gst_courses = [
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2, 'level': 100},
        {'code': 'GST102', 'title': 'Nigerian Peoples and Culture', 'unit': 2, 'level': 100},
        {'code': 'GST201', 'title': 'Entrepreneurship', 'unit': 2, 'level': 200},
    ]
    
    # Create GST courses once (assign to first department)
    first_dept = list(departments.values())[0] if departments else None
    if first_dept:
        for gst in gst_courses:
            level = levels[gst['level']]
            course, created = Course.objects.get_or_create(
                code=gst['code'],
                defaults={
                    'title': gst['title'],
                    'credit_unit': gst['unit'],
                    'department': first_dept,
                    'level': level,
                    'semester': first_semester_2025,
                    'is_elective': False,
                }
            )
            courses[gst['code']] = course
            if created:
                print(f"    Created: {course.code} - {course.title}")
    
    # Create department-specific courses
    for dept_code, department in departments.items():
        if dept_code in COURSES_DATA:
            for course_data in COURSES_DATA[dept_code]:
                # Skip GST courses (already created above)
                if course_data['code'].startswith('GST'):
                    continue
                    
                level = levels[course_data['level']]
                # Assign semester based on course code
                if '101' in course_data['code'] or '201' in course_data['code'] or '301' in course_data['code'] or '401' in course_data['code']:
                    semester = first_semester_2025
                else:
                    semester = second_semester_2025
                    
                course, created = Course.objects.get_or_create(
                    code=course_data['code'],
                    department=department,
                    defaults={
                        'title': course_data['title'],
                        'credit_unit': course_data['unit'],
                        'level': level,
                        'semester': semester,
                        'is_elective': False,
                    }
                )
                courses[course_data['code']] = course
                if created:
                    print(f"    Created: {course.code} - {course.title}")
    
    print(f"  Total courses created: {len(courses)}")
    return courses

def get_courses_for_student(student, expected_level):
    department = student.department
    try:
        level_obj = Level.objects.get(level=expected_level)
    except Level.DoesNotExist:
        return []
    courses = list(Course.objects.filter(department=department, level=level_obj))
    gst_courses = list(Course.objects.filter(code__startswith='GST', level=level_obj))
    courses.extend(gst_courses)
    courses = list({c.id: c for c in courses}.values())
    return courses

def create_results_for_student(student, semesters):
    total_results_created = 0
    semester_data = []
    
    for semester in semesters:
        session_year = int(semester.session.name.split('/')[0])
        admission_year = student.admission_year
        years_elapsed = session_year - admission_year
        if years_elapsed < 0:
            continue
        
        if years_elapsed == 0:
            expected_level = 100
        else:
            expected_level = 100 + (years_elapsed * 100)
        if expected_level > 500:
            continue
        
        courses = get_courses_for_student(student, expected_level)
        if not courses:
            continue
        
        num_courses = min(random.randint(5, 8), len(courses))
        selected_courses = random.sample(courses, num_courses)
        
        results_data = []
        for course in selected_courses:
            ca_score = random.randint(20, 40)
            exam_score = random.randint(20, 70)
            grade = calculate_grade(ca_score + exam_score)
            result, created = Result.objects.update_or_create(
                student=student,
                course=course,
                semester=semester,
                defaults={
                    'ca_score': ca_score,
                    'exam_score': exam_score,
                    'is_published': random.choice([True, False]),
                    'published_at': datetime.now() if random.choice([True, False]) else None,
                }
            )
            if created:
                total_results_created += 1
            results_data.append({
                'credit_unit': course.credit_unit,
                'grade': grade
            })
        
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
    
    return len(semester_data), total_results_created

def get_semesters_for_student(student):
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

def assign_lecturers_to_courses(courses, lecturers):
    print("\nAssigning Lecturers to Courses...")
    course_list = list(courses.values())
    assignments = 0
    for lecturer in lecturers:
        num_courses = min(random.randint(2, 4), len(course_list))
        assigned = random.sample(course_list, num_courses)
        for course in assigned:
            course.lecturer = lecturer
            course.save()
            assignments += 1
            print(f"  Assigned {lecturer.get_full_name()} to {course.code}")
    print(f"  Total assignments: {assignments}")

def create_course_registrations(students, courses):
    print("\nCreating Course Registrations...")
    registrations_created = 0
    current_semester = Semester.get_current()
    if not current_semester:
        print("  No current semester found, skipping registrations")
        return
    
    course_list = list(courses.values())
    for student in students:
        num_courses = min(random.randint(4, 6), len(course_list))
        selected = random.sample(course_list, num_courses)
        for course in selected:
            reg, created = CourseRegistration.objects.get_or_create(
                student=student,
                course=course,
                semester=current_semester
            )
            if created:
                registrations_created += 1
        if (student.id % 20) == 0:
            print(f"  Registered {student.id} students...")
    print(f"  Total registrations: {registrations_created}")

# ============================================================
# MAIN FUNCTION
# ============================================================
def main():
    print("=" * 70)
    print("CUSTOM DATABASE POPULATION")
    print("=" * 70)
    print(f"  Students: {NUM_STUDENTS}")
    print(f"  Lecturers: {NUM_LECTURERS}")
    print(f"  Admins: {NUM_ADMINS}")
    print(f"  Super Admin: 1")
    print(f"  All passwords: {PASSWORD}")
    print("=" * 70)
    
    if NON_INTERACTIVE:
        print("\nRunning in non-interactive mode...")
    else:
        response = input("\nThis will reset and populate the database. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    try:
        with transaction.atomic():
            print("\n[STEP 1] Clearing existing data...")
            if NON_INTERACTIVE:
                should_clear = True
            else:
                should_clear = input("  Clear all existing data? (y/n): ").lower() == 'y'
            
            if should_clear:
                Result.objects.all().delete()
                SemesterGPARecord.objects.all().delete()
                CGPARecord.objects.all().delete()
                CourseRegistration.objects.all().delete()
                StudentProfile.objects.all().delete()
                User.objects.filter(role__in=['student', 'lecturer', 'admin']).exclude(is_superuser=True).delete()
                print("  Existing data cleared.")
            else:
                print("  Keeping existing data.")
            
            print("\n[STEP 2] Creating Academic Structure...")
            faculties, departments = create_faculties_and_departments()
            levels = create_levels()
            sessions = create_academic_sessions()
            semesters = create_semesters(sessions)
            
            print("\n[STEP 3] Creating Users...")
            super_admin = create_super_admin()
            admins = create_admin_users()
            lecturers = create_lecturer_users()
            students = create_students(departments, levels)
            
            print("\n[STEP 4] Creating Courses...")
            courses = create_courses(departments, levels, semesters)
            
            assign_lecturers_to_courses(courses, lecturers)
            
            create_course_registrations(students, courses)
            
            print("\n[STEP 5] Creating Results for Students...")
            total_students_processed = 0
            total_semesters_processed = 0
            total_results_created = 0
            
            for idx, student in enumerate(students):
                if (idx + 1) % 10 == 0:
                    print(f"\n[{idx + 1}/{len(students)}] {student.matric_no}")
                semesters_list = get_semesters_for_student(student)
                if semesters_list:
                    sem_count, res_count = create_results_for_student(student, semesters_list)
                    total_semesters_processed += sem_count
                    total_results_created += res_count
                    total_students_processed += 1
            
            print("\n" + "=" * 70)
            print("POPULATION COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            print(f"  Faculties: {len(faculties)}")
            print(f"  Departments: {len(departments)}")
            print(f"  Levels: {len(levels)}")
            print(f"  Academic Sessions: {len(sessions)}")
            print(f"  Semesters: {len(semesters)}")
            print(f"  Super Admin: 1")
            print(f"  School Admins: {len(admins)}")
            print(f"  Lecturers: {len(lecturers)}")
            print(f"  Students: {len(students)}")
            print(f"  Courses: {len(courses)}")
            print(f"  Results Created: {total_results_created}")
            print(f"  Total Results in DB: {Result.objects.count()}")
            print(f"  GPA Records: {SemesterGPARecord.objects.count()}")
            print(f"  CGPA Records: {CGPARecord.objects.count()}")
            print(f"  Course Registrations: {CourseRegistration.objects.count()}")
            print("=" * 70)
            print("\nLOGIN CREDENTIALS:")
            print(f"  Super Admin: admin@gmail.com")
            print(f"  All passwords: {PASSWORD}")
            print("=" * 70)
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()