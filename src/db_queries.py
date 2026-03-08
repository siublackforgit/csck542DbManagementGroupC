"""
Raw SQL query
"""

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

# Import DB credentials from sibling module (PEP-8 relative import)
from src.db_connection import DB_CONFIG


def connect_db():
    """Establish a raw MySQL connection using credentials from db_credentials.py.

    Returns:
        mysql.connector.connection.MySQLConnection: Active DB connection object
        None: If connection fails (error message shown to user)
    """
    try:
        # Unpack config dict for clean connection (PEP-8 line length compliant)
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        # User-friendly error message (PEP-8 string formatting)
        messagebox.showerror(
            "DB Connection Error",
            f"Failed to connect to MySQL:\n{str(e)}"
        )
        return None


def get_students_in_course_by_lecturer(course_code, lecturer_name):
    """Retrieve students enrolled in a specific course taught by a lecturer.

    Args:
        course_code (str): Code of the target course (e.g., "CS101")
        lecturer_name (str): Full name of the lecturer (e.g., "Dr. Alice Smith")

    Returns:
        list: List of tuples containing (student_id, student_name, program_name)
    """
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()
    # Raw SQL query (formatted for readability, PEP-8 line length)
    sql_query = """
    SELECT s.student_id, s.name, p.program_name 
    FROM students s
    JOIN student_course_enrolments sce ON s.student_id = sce.student_id
    JOIN course_lecturers cl ON sce.course_code = cl.course_code
    JOIN lecturers l ON cl.lecturer_id = l.lecturer_id
    LEFT JOIN programs p ON s.program_id = p.program_id
    WHERE sce.course_code = %s AND l.name = %s
    """

    try:
        cursor.execute(sql_query, (course_code, lecturer_name))
        results = cursor.fetchall()
    finally:
        # Ensure resources are closed (PEP-8 best practice)
        cursor.close()
        conn.close()

    return results


def get_top_final_year_students(min_avg=70):
    """Retrieve final-year students with average grade above a threshold.

    Args:
        min_avg (int): Minimum average grade percentage (default: 70)

    Returns:
        list: List of tuples containing (student_id, name, avg_grade, program_name)
    """
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()
    sql_query = """
    SELECT s.student_id, s.name, ROUND(AVG(sg.grade), 2) AS avg_grade, p.program_name
    FROM students s
    JOIN student_grades sg ON s.student_id = sg.student_id
    JOIN programs p ON s.program_id = p.program_id
    WHERE s.year_of_study = p.duration_years
    GROUP BY s.student_id, s.name, p.program_name
    HAVING AVG(sg.grade) > %s
    """

    try:
        cursor.execute(sql_query, (min_avg,))
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return results


def get_students_no_current_courses(semester):
    """Retrieve students with no course enrolments in the current semester.

    Args:
        semester (str): Target semester (e.g., "2024-1")

    Returns:
        list: List of tuples containing (student_id, name, program_name)
    """
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()
    sql_query = """
    SELECT s.student_id, s.name, p.program_name 
    FROM students s
    LEFT JOIN student_course_enrolments sce 
        ON s.student_id = sce.student_id AND sce.semester = %s
    JOIN programs p ON s.program_id = p.program_id
    WHERE sce.student_id IS NULL
    """

    try:
        cursor.execute(sql_query, (semester,))
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return results


def get_student_advisor(student_id):
    """Retrieve faculty advisor details for a specific student.

    Args:
        student_id (int): Unique ID of the target student

    Returns:
        list: List of tuples containing (advisor_name, expertise, student_contact)
    """
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()
    sql_query = """
    SELECT l.name AS advisor_name, l.areas_of_expertise, s.contact_info AS student_contact
    FROM students s
    LEFT JOIN lecturers l ON s.faculty_advisor_id = l.lecturer_id
    WHERE s.student_id = %s
    """

    try:
        cursor.execute(sql_query, (student_id,))
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return results


def get_lecturers_by_research_area(area):
    """Retrieve lecturers with expertise in a specific research area (partial match).

    Args:
        area (str): Research area to search (e.g., "AI", "Database Systems")

    Returns:
        list: List of tuples containing (lecturer_id, name, department, expertise)
    """
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()
    sql_query = """
    SELECT l.lecturer_id, l.name, d.department_name, l.areas_of_expertise
    FROM lecturers l
    JOIN departments d ON l.department_id = d.department_id
    WHERE l.areas_of_expertise LIKE %s
    """

    try:
        # Partial match (case-insensitive) for flexibility
        cursor.execute(sql_query, (f"%{area}%",))
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return results