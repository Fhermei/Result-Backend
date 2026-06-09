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
from faker import Faker
from apps.academics.models import Faculty, Department, AcademicSession, Semester, Level
from apps.courses.models import Course, CourseRegistration
from apps.students.models import StudentProfile
from apps.results.models import Result, SemesterGPARecord, CGPARecord

User = get_user_model()
fake = Faker('en_NG')

NON_INTERACTIVE = '--non-interactive' in sys.argv
if NON_INTERACTIVE:
    sys.argv.remove('--non-interactive')

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

COURSES_DATA = {
    'CSC': [
        {'code': 'CSC101', 'title': 'Introduction to Computer Science', 'unit': 3},
        {'code': 'CSC102', 'title': 'Programming in C', 'unit': 3},
        {'code': 'CSC201', 'title': 'Data Structures', 'unit': 3},
        {'code': 'CSC202', 'title': 'Object Oriented Programming', 'unit': 3},
        {'code': 'CSC203', 'title': 'Database Management Systems', 'unit': 3},
        {'code': 'CSC204', 'title': 'Operating Systems', 'unit': 3},
        {'code': 'CSC301', 'title': 'Software Engineering', 'unit': 3},
        {'code': 'CSC302', 'title': 'Computer Networks', 'unit': 3},
        {'code': 'CSC303', 'title': 'Web Development', 'unit': 3},
        {'code': 'CSC401', 'title': 'Artificial Intelligence', 'unit': 3},
        {'code': 'CSC402', 'title': 'Project Management', 'unit': 2},
        {'code': 'CSC403', 'title': 'Final Year Project', 'unit': 6},
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2},
        {'code': 'GST102', 'title': 'Nigerian Peoples and Culture', 'unit': 2},
        {'code': 'MTH101', 'title': 'General Mathematics I', 'unit': 3},
        {'code': 'MTH102', 'title': 'General Mathematics II', 'unit': 3},
        {'code': 'PHY101', 'title': 'General Physics I', 'unit': 3},
        {'code': 'PHY102', 'title': 'General Physics II', 'unit': 3},
    ],
    'CEN': [
        {'code': 'CEN101', 'title': 'Computer Engineering Fundamentals', 'unit': 3},
        {'code': 'CEN102', 'title': 'Digital Logic Design', 'unit': 3},
        {'code': 'CEN201', 'title': 'Microprocessors', 'unit': 3},
        {'code': 'CEN202', 'title': 'Computer Architecture', 'unit': 3},
        {'code': 'CEN301', 'title': 'Embedded Systems', 'unit': 3},
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2},
        {'code': 'MTH101', 'title': 'Engineering Mathematics I', 'unit': 3},
    ],
    'ECO': [
        {'code': 'ECO101', 'title': 'Principles of Economics I', 'unit': 3},
        {'code': 'ECO102', 'title': 'Principles of Economics II', 'unit': 3},
        {'code': 'ECO201', 'title': 'Microeconomic Theory', 'unit': 3},
        {'code': 'ECO202', 'title': 'Macroeconomic Theory', 'unit': 3},
        {'code': 'ECO301', 'title': 'Econometrics', 'unit': 3},
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2},
        {'code': 'GST102', 'title': 'Nigerian Peoples and Culture', 'unit': 2},
    ],
    'ACC': [
        {'code': 'ACC101', 'title': 'Introduction to Accounting', 'unit': 3},
        {'code': 'ACC102', 'title': 'Financial Accounting I', 'unit': 3},
        {'code': 'ACC201', 'title': 'Financial Accounting II', 'unit': 3},
        {'code': 'ACC202', 'title': 'Cost Accounting', 'unit': 3},
        {'code': 'ACC301', 'title': 'Management Accounting', 'unit': 3},
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2},
    ],
    'BUS': [
        {'code': 'BUS101', 'title': 'Introduction to Business', 'unit': 3},
        {'code': 'BUS102', 'title': 'Principles of Management', 'unit': 3},
        {'code': 'BUS201', 'title': 'Organizational Behaviour', 'unit': 3},
        {'code': 'BUS202', 'title': 'Business Communication', 'unit': 2},
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2},
    ],
    'LAW': [
        {'code': 'LAW101', 'title': 'Nigerian Legal System', 'unit': 3},
        {'code': 'LAW102', 'title': 'Law of Contract', 'unit': 3},
        {'code': 'LAW201', 'title': 'Constitutional Law', 'unit': 3},
        {'code': 'LAW202', 'title': 'Criminal Law', 'unit': 3},
        {'code': 'GST101', 'title': 'Use of English', 'unit': 2},
    ],
}

def calculate_semester_gpa(results_data):
    total_quality_points = 0
    total_credit_units = 0
    grade_points = {'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0}
    for result in results_data:
        credit_unit = result['credit_unit']
        grade = result['grade']
        quality_points = credit_unit * grade_points.get(grade, 0)
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

def create_faculties_and_departments():
    print("Creating Faculties and Departments...")
    faculties = {}
    departments = {}
    for faculty_data in FACULTIES_DATA:
        faculty, created = Faculty.objects.get_or_create(
            code=faculty_data['code'],
            defaults={'name': faculty_data['name']}
        )
        faculties[faculty_data['code']] = faculty
        for dept_data in faculty_data['departments']:
            department, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name'], 'faculty': faculty}
            )
            departments[dept_data['code']] = department
            print(f"  Created: {faculty.name} -> {department.name}")
    return faculties, departments

def create_levels():
    print("\nCreating Levels...")
    levels = {}
    for level_value in [100, 200, 300, 400, 500]:
        level, created = Level.objects.get_or_create(level=level_value)
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
    for session_data in sessions_data:
        session, created = AcademicSession.objects.get_or_create(
            name=session_data['name'],
            defaults={
                'start_date': session_data['start'],
                'end_date': session_data['end'],
                'is_current': session_data.get('is_current', False)
            }
        )
        sessions[session_data['name']] = session
        print(f"  Created: {session.name}")
    return sessions

def create_semesters(sessions):
    print("\nCreating Semesters...")
    semesters = {}
    for session_name, session in sessions.items():
        for sem_name, sem_display in [('first', 'First Semester'), ('second', 'Second Semester')]:
            is_current = (session_name == '2025/2026' and sem_name == 'first')
            semester, created = Semester.objects.get_or_create(
                session=session,
                name=sem_name,
                defaults={'is_current': is_current}
            )
            semesters[f"{session_name}_{sem_name}"] = semester
            print(f"  Created: {session.name} - {sem_display}")
    return semesters

def create_admin_users():
    print("\nCreating Admin Users...")
    admins = []
    admin_emails = [
        'admin@gmail.com', 'registrar@university.edu.ng', 'dean_engineering@university.edu.ng',
        'dean_science@university.edu.ng', 'dean_social_sciences@university.edu.ng',
        'dean_arts@university.edu.ng', 'dean_management@university.edu.ng',
        'dean_law@university.edu.ng', 'hod_csc@university.edu.ng', 'hod_accounting@university.edu.ng'
    ]
    admin_names = [
        ('Admin', 'User'), ('Dr. Ade', 'Ogunleye'), ('Prof. Ngozi', 'Okonkwo'),
        ('Prof. Olufemi', 'Adewale'), ('Dr. Chiamaka', 'Eze'), ('Prof. Adebayo', 'Okafor'),
        ('Dr. Funmilayo', 'Balogun'), ('Prof. Chukwudi', 'Nwosu'), ('Dr. Similoluwa', 'Ogundipe'),
        ('Dr. Oluwatobi', 'Adebayo')
    ]
    for i, (first_name, last_name) in enumerate(admin_names):
        email = admin_emails[i] if i < len(admin_emails) else f"admin{i}@university.edu.ng"
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': 'admin',
                'is_staff': True,
                'is_superuser': (email == 'admin@gmail.com')
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            admins.append(user)
            print(f"  Created Admin: {first_name} {last_name} ({email})")
    return admins

def create_lecturer_users():
    print("\nCreating Lecturer Users...")
    lecturers = []
    lecturer_first_names = [
        'Dr. Chinedu', 'Prof. Oluwaseun', 'Dr. Nkechi', 'Prof. Emeka', 'Dr. Temitope',
        'Prof. Chinonso', 'Dr. Adeola', 'Prof. Ifeanyi', 'Dr. Oluwafemi', 'Prof. Chinwe',
        'Dr. Segun', 'Prof. Adaobi', 'Dr. Okechukwu', 'Prof. Oluwadamilola', 'Dr. Chukwuma',
        'Prof. Oluwatoyin', 'Dr. Nneka', 'Prof. Onyekachi', 'Dr. Oluwafunmilayo', 'Prof. Chukwudi',
        'Dr. Oluwaseyi', 'Prof. Chimamanda', 'Dr. Oluwole', 'Prof. Ngozi', 'Dr. Oluwatosin',
        'Prof. Chibueze', 'Dr. Oluwaseun', 'Prof. Chiamaka', 'Dr. Oluwakemi', 'Prof. Olumide'
    ]
    lecturer_last_names = [
        'Okafor', 'Adewale', 'Eze', 'Okonkwo', 'Balogun', 'Nwosu', 'Ogunleye',
        'Chukwu', 'Oladipo', 'Nwachukwu', 'Oyedele', 'Okeke', 'Ogunbiyi', 'Nwankwo',
        'Ogunyemi', 'Ekwueme', 'Ogunlana', 'Nweke', 'Ogunwale', 'Okpara', 'Ogunjobi',
        'Nwagwu', 'Ogunlade', 'Okoro', 'Ogunmuyiwa', 'Nwaka', 'Ogunbanwo', 'Nwagbara'
    ]
    for i in range(30):
        first_name = lecturer_first_names[i % len(lecturer_first_names)]
        last_name = lecturer_last_names[i % len(lecturer_last_names)]
        email = f"lecturer.{first_name.lower().replace(' ', '')}.{last_name.lower()}@university.edu.ng"
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
            lecturers.append(user)
            print(f"  Created Lecturer {i+1}: {first_name} {last_name}")
    return lecturers

def create_students(departments, levels, total_students=2000):
    print(f"\nCreating {total_students} Student Users...")
    students = []
    admission_years = [2020, 2021, 2022, 2023, 2024, 2025]
    departments_list = list(departments.values())
    for i in range(total_students):
        first_name = random.choice(NIGERIAN_FIRST_NAMES)
        last_name = random.choice(NIGERIAN_LAST_NAMES)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@student.edu.ng"
        matric_no = f"U{random.randint(20, 25)}/{random.choice(['01', '02', '03', '04', '05'])}/{str(i+10000).zfill(4)}"
        admission_year = random.choice(admission_years)
        current_year = 2025
        years_elapsed = current_year - admission_year
        if years_elapsed >= 4:
            level_value = 400
        elif years_elapsed == 3:
            level_value = 300
        elif years_elapsed == 2:
            level_value = 200
        elif years_elapsed == 1:
            level_value = 100
        else:
            level_value = 100
        level = levels.get(level_value, levels[100])
        department = random.choice(departments_list)
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'role': 'student'
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            student, created = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'matric_no': matric_no,
                    'department': department,
                    'current_level': level,
                    'admission_year': admission_year
                }
            )
            students.append(student)
            if (i + 1) % 200 == 0:
                print(f"  Created {i + 1} students...")
    print(f"  Successfully created {len(students)} students")
    return students

def create_courses(departments, levels, semesters):
    print("\nCreating Courses...")
    courses = {}
    first_semester_2025 = semesters.get('2025/2026_first')
    second_semester_2025 = semesters.get('2025/2026_second')
    for dept_code, department in departments.items():
        if dept_code in COURSES_DATA:
            for course_data in COURSES_DATA[dept_code]:
                if '101' in course_data['code'] or '102' in course_data['code']:
                    level = levels[100]
                elif '201' in course_data['code'] or '202' in course_data['code'] or '203' in course_data['code'] or '204' in course_data['code']:
                    level = levels[200]
                elif '301' in course_data['code'] or '302' in course_data['code'] or '303' in course_data['code']:
                    level = levels[300]
                else:
                    level = levels[400]
                if '101' in course_data['code'] or '201' in course_data['code'] or '301' in course_data['code'] or '401' in course_data['code']:
                    semester = first_semester_2025
                else:
                    semester = second_semester_2025
                course, created = Course.objects.get_or_create(
                    code=course_data['code'],
                    defaults={
                        'title': course_data['title'],
                        'credit_unit': course_data['unit'],
                        'department': department,
                        'level': level,
                        'semester': semester,
                        'is_elective': 'GST' not in course_data['code']
                    }
                )
                courses[course_data['code']] = course
                print(f"  Created: {course.code} - {course.title} ({course.credit_unit} units)")
    return courses

def create_results(students, courses, semesters, sessions):
    print("\nCreating Results for Students...")
    results_created = 0
    semester_objects = list(semesters.values())
    for student in students[:500]:
        for semester in semester_objects:
            student_level = student.current_level.level
            relevant_courses = [c for c in courses.values() if c.level.level == student_level]
            if not relevant_courses:
                continue
            num_courses = random.randint(6, 8)
            selected_courses = random.sample(relevant_courses, min(num_courses, len(relevant_courses)))
            results_data = []
            for course in selected_courses:
                ca_score = random.randint(20, 40)
                exam_score = random.randint(20, 70)
                result, created = Result.objects.get_or_create(
                    student=student,
                    course=course,
                    semester=semester,
                    defaults={
                        'ca_score': ca_score,
                        'exam_score': exam_score,
                        'is_published': True
                    }
                )
                if created:
                    results_created += 1
                    results_data.append({
                        'credit_unit': course.credit_unit,
                        'total_score': float(result.total_score),
                        'grade': result.grade
                    })
            if results_data:
                gpa, total_qp, total_cu = calculate_semester_gpa(results_data)
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
            if results_created % 500 == 0 and results_created > 0:
                print(f"  Created {results_created} results...")
    print(f"  Successfully created {results_created} results")

def calculate_all_cgpa(students):
    print("\nCalculating CGPA for all students...")
    for student in students:
        gpa_records = SemesterGPARecord.objects.filter(student=student)
        if not gpa_records:
            continue
        semester_data = []
        for record in gpa_records:
            semester_data.append({
                'total_quality_points': float(record.total_quality_points),
                'total_credit_units': record.total_credit_units
            })
        cgpa = calculate_cgpa(semester_data)
        class_degree = get_class_degree(cgpa)
        total_qp = sum(float(r.total_quality_points) for r in gpa_records)
        total_cu = sum(r.total_credit_units for r in gpa_records)
        CGPARecord.objects.update_or_create(
            student=student,
            defaults={
                'cgpa': cgpa,
                'total_quality_points_all': total_qp,
                'total_credit_units_all': total_cu,
                'class_degree': class_degree
            }
        )
    print(f"  Calculated CGPA for {len(students)} students")

def main():
    print("=" * 60)
    print("POPULATING NIGERIAN UNIVERSITY RESULT MANAGEMENT SYSTEM")
    print("=" * 60)
    if NON_INTERACTIVE:
        print("Running in non-interactive mode...")
    else:
        response = input("This will populate the database with sample data. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    try:
        with transaction.atomic():
            faculties, departments = create_faculties_and_departments()
            levels = create_levels()
            sessions = create_academic_sessions()
            semesters = create_semesters(sessions)
            admins = create_admin_users()
            lecturers = create_lecturer_users()
            students = create_students(departments, levels, total_students=2000)
            courses = create_courses(departments, levels, semesters)
            create_results(students, courses, semesters, sessions)
            calculate_all_cgpa(students)
            print("\n" + "=" * 60)
            print("POPULATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"  Faculties: {len(faculties)}")
            print(f"  Departments: {len(departments)}")
            print(f"  Levels: {len(levels)}")
            print(f"  Academic Sessions: {len(sessions)}")
            print(f"  Semesters: {len(semesters)}")
            print(f"  Admin Users: {len(admins)}")
            print(f"  Lecturer Users: {len(lecturers)}")
            print(f"  Student Users: {len(students)}")
            print(f"  Courses: {len(courses)}")
            print("=" * 60)
            print("\nLogin Credentials:")
            print("  Admin email: admin@gmail.com")
            print("  All passwords: admin123")
            print("=" * 60)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()