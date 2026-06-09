"""
GPA and CGPA Calculation Engine for Nigerian Universities
Using NUC 5-point Grading Scale
"""

GRADE_POINTS = {
    'A': 5.0,
    'B': 4.0,
    'C': 3.0,
    'D': 2.0,
    'E': 1.0,
    'F': 0.0,
}

GRADE_BY_SCORE = [
    (70, 'A'),
    (60, 'B'),
    (50, 'C'),
    (45, 'D'),
    (40, 'E'),
    (0, 'F'),
]


def calculate_grade(score):
    """Calculate letter grade based on score (0-100)"""
    for min_score, grade in GRADE_BY_SCORE:
        if score >= min_score:
            return grade
    return 'F'


def calculate_quality_points(credit_unit, grade):
    """Calculate quality points for a course"""
    return credit_unit * GRADE_POINTS.get(grade, 0)


def calculate_semester_gpa(results):
    """
    Calculate GPA for a semester
    results: list of dict with 'credit_unit' and 'total_score' (or 'grade')
    Returns: (gpa, total_quality_points, total_credit_units)
    """
    total_quality_points = 0
    total_credit_units = 0
    
    for result in results:
        credit_unit = result['credit_unit']
        if 'grade' in result:
            grade = result['grade']
        else:
            grade = calculate_grade(result['total_score'])
        
        if grade != 'F':  # F grade still counts in total units but gives 0 quality points
            quality_points = calculate_quality_points(credit_unit, grade)
        else:
            quality_points = 0
        
        total_quality_points += quality_points
        total_credit_units += credit_unit
    
    if total_credit_units == 0:
        return 0.0, 0, 0
    
    gpa = total_quality_points / total_credit_units
    return round(gpa, 2), total_quality_points, total_credit_units


def calculate_cgpa(all_semester_data):
    """
    Calculate CGPA across multiple semesters
    all_semester_data: list of dict with 'total_quality_points' and 'total_credit_units'
    Returns: cgpa
    """
    total_quality_points_all = sum(s['total_quality_points'] for s in all_semester_data)
    total_credit_units_all = sum(s['total_credit_units'] for s in all_semester_data)
    
    if total_credit_units_all == 0:
        return 0.0
    
    cgpa = total_quality_points_all / total_credit_units_all
    return round(cgpa, 2)


def get_class_degree(cgpa):
    """
    Get degree classification based on CGPA
    Nigerian University NUC Standard
    """
    if cgpa >= 4.50:
        return 'First Class'
    elif cgpa >= 3.50:
        return 'Second Class Upper'
    elif cgpa >= 2.40:
        return 'Second Class Lower'
    elif cgpa >= 1.50:
        return 'Third Class'
    elif cgpa >= 1.00:
        return 'Pass'
    else:
        return 'Probation'


def calculate_total_cgpa_for_student(student, semester_results):
    """
    Complete CGPA calculation for a student across all semesters
    semester_results: dict with semester_id as key and list of results
    """
    semester_data = []
    
    for semester_id, results in semester_results.items():
        gpa, tqp, tcu = calculate_semester_gpa(results)
        semester_data.append({
            'semester_id': semester_id,
            'gpa': gpa,
            'total_quality_points': tqp,
            'total_credit_units': tcu,
            'results': results
        })
    
    cgpa = calculate_cgpa(semester_data)
    class_degree = get_class_degree(cgpa)
    
    return {
        'cgpa': cgpa,
        'class_degree': class_degree,
        'semesters': semester_data
    }