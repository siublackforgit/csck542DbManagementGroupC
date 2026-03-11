# app/db/queries.py
def get_query_definitions():
    return {
        "1. Students enrolled in a specific course taught by a particular lecturer": {
            "description": "Returns students enrolled in the chosen course where the course is assigned to the selected lecturer.",
            "filters": ["course", "lecturer"],
            "sql": """
                SELECT
                    s.student_id,
                    s.name AS student_name,
                    c.course_code,
                    c.course_name,
                    l.name AS lecturer_name
                FROM students s
                JOIN enrolment e ON s.student_id = e.student_id
                JOIN courses c ON e.course_code = c.course_code
                JOIN courselecturers cl ON c.course_code = cl.course_code
                JOIN lecturers l ON cl.lecturer_id = l.lecturer_id
                WHERE (%s = 'All' OR c.course_name = %s)
                  AND (%s = 'All' OR l.name = %s)
                ORDER BY s.name;
            """,
            "params": lambda f: (f["course"], f["course"], f["lecturer"], f["lecturer"])
        },

        "2. Students with average grade above 70% (final year)": {
            "description": "Lists final-year students whose average numeric grade is above 70%.",
            "filters": ["program"],
            "sql": """
                SELECT
                    s.student_id,
                    s.name,
                    p.programme_name,
                    s.year_of_study,
                    ROUND(AVG(a.assessment_grade), 2) AS average_grade
                FROM students s
                LEFT JOIN programmes p ON s.programme_id = p.programme_id
                JOIN enrolment e ON s.student_id = e.student_id
                JOIN assessments a ON e.enrolment_id = a.enrolment_id
                WHERE (%s = 'All' OR p.programme_name = %s)
                  AND s.year_of_study = (SELECT MAX(year_of_study) FROM students)
                  AND a.assessment_grade IS NOT NULL
                GROUP BY s.student_id, s.name, p.programme_name, s.year_of_study
                HAVING AVG(a.assessment_grade) > 70
                ORDER BY average_grade DESC, s.name;
            """,
            "params": lambda f: (f["program"], f["program"])
        },

        "3. Students not registered in any course (current semester)": {
            "description": "Finds students who do not have any enrollment record for the current semester.",
            "filters": ["program"],
            "sql": """
                SELECT
                    s.student_id,
                    s.name,
                    s.email,
                    p.programme_name
                FROM students s
                LEFT JOIN programmes p ON s.programme_id = p.programme_id
                WHERE (%s = 'All' OR p.programme_name = %s)
                  AND s.student_id NOT IN (
                      SELECT DISTINCT student_id
                      FROM enrolment
                  )
                ORDER BY s.name;
            """,
            "params": lambda f: (f["program"], f["program"])
        },

        "4. Faculty advisor contact info for a specific student": {
            "description": "Returns advisor details for the selected student (uses advisor_id in students table).",
            "filters": ["student"],
            "sql": """
                SELECT
                    s.name AS student_name,
                    l.name AS advisor_name,
                    d.department_name,
                    d.faculty
                FROM students s
                JOIN lecturers l ON s.advisor_id = l.lecturer_id
                LEFT JOIN departments d ON l.department_id = d.department_id
                WHERE (%s = 'All' OR s.name = %s)
                ORDER BY s.name;
            """,
            "params": lambda f: (f["student"], f["student"])
        },

        "5. Lecturers with expertise in a particular area": {
            "description": "Lists lecturers whose expertise matches the selected research area.",
            "filters": ["expertise"],
            "sql": """
                SELECT
                    l.lecturer_id,
                    l.name,
                    le.area_name AS expertise_area,
                    d.department_name
                FROM lecturers l
                JOIN lecturerexpertise le ON l.lecturer_id = le.lecturer_id
                LEFT JOIN departments d ON l.department_id = d.department_id
                WHERE (%s = 'All' OR le.area_name = %s)
                ORDER BY l.name;
            """,
            "params": lambda f: (f["expertise"], f["expertise"])
        },

        "6. Courses taught by lecturers in a specific department": {
            "description": "Shows all courses offered by lecturers from the selected department.",
            "filters": ["department"],
            "sql": """
                SELECT DISTINCT
                    c.course_code,
                    c.course_name,
                    l.name AS lecturer_name,
                    d.department_name
                FROM courses c
                JOIN courselecturers cl ON c.course_code = cl.course_code
                JOIN lecturers l ON cl.lecturer_id = l.lecturer_id
                JOIN departments d ON l.department_id = d.department_id
                WHERE (%s = 'All' OR d.department_name = %s)
                ORDER BY c.course_name;
            """,
            "params": lambda f: (f["department"], f["department"])
        },

        "7. Lecturers who supervised the most research projects": {
            "description": "Ranks lecturers by the number of research projects they supervise (principal investigator).",
            "filters": [],
            "sql": """
                SELECT
                    l.lecturer_id,
                    l.name AS lecturer_name,
                    COUNT(rp.project_id) AS total_projects,
                    d.department_name
                FROM lecturers l
                LEFT JOIN researchprojects rp
                    ON l.lecturer_id = rp.principal_investigator_id
                LEFT JOIN departments d ON l.department_id = d.department_id
                GROUP BY l.lecturer_id, l.name, d.department_name
                ORDER BY total_projects DESC, l.name;
            """,
            "params": lambda f: ()
        },

        "8. Lecturer publications (past year)": {
            "description": "Shows publications by lecturers from the past 12 months.",
            "filters": ["lecturer"],
            "sql": """
                SELECT
                    l.name AS lecturer_name,
                    p.title AS publication_title,
                    p.publication_date,
                    rp.project_title AS research_project
                FROM publications p
                JOIN lecturers l ON p.lecturer_id = l.lecturer_id
                JOIN researchprojects rp ON p.project_id = rp.project_id
                WHERE (%s = 'All' OR l.name = %s)
                  AND p.publication_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                ORDER BY p.publication_date DESC;
            """,
            "params": lambda f: (f["lecturer"], f["lecturer"])
        },

        "9. Students advised by a specific lecturer": {
            "description": "Lists all students supervised/advised by the selected lecturer.",
            "filters": ["lecturer"],
            "sql": """
                SELECT
                    l.name AS advisor_name,
                    s.student_id,
                    s.name AS student_name,
                    s.email,
                    s.year_of_study
                FROM students s
                JOIN lecturers l ON s.advisor_id = l.lecturer_id
                WHERE (%s = 'All' OR l.name = %s)
                ORDER BY s.name;
            """,
            "params": lambda f: (f["lecturer"], f["lecturer"])
        },

        "10. All staff in a specific department": {
            "description": "Lists all non-academic staff members employed in the selected department.",
            "filters": ["department"],
            "sql": """
                SELECT
                    nas.staff_id,
                    nas.name,
                    nas.job_title,
                    nas.employment_type,
                    d.department_name,
                    nas.salary_info
                FROM nonacademicstaff nas
                JOIN departments d ON nas.department_id = d.department_id
                WHERE (%s = 'All' OR d.department_name = %s)
                ORDER BY nas.name;
            """,
            "params": lambda f: (f["department"], f["department"])
        },

        "11. Employees supervising students in a particular program": {
            "description": "Identifies lecturers/staff who supervise students in the selected program.",
            "filters": ["program"],
            "sql": """
                SELECT DISTINCT
                    l.lecturer_id,
                    l.name AS supervisor_name,
                    p.programme_name,
                    d.department_name,
                    COUNT(s.student_id) AS total_students_supervised
                FROM lecturers l
                JOIN students s ON l.lecturer_id = s.advisor_id
                JOIN programmes p ON s.programme_id = p.programme_id
                JOIN departments d ON l.department_id = d.department_id
                WHERE (%s = 'All' OR p.programme_name = %s)
                GROUP BY l.lecturer_id, l.name, p.programme_name, d.department_name
                ORDER BY total_students_supervised DESC;
            """,
            "params": lambda f: (f["program"], f["program"])
        }
    }

def get_role_permissions():
    return {
        "Student": [
            "1. Students enrolled in a specific course taught by a particular lecturer",
            "3. Students not registered in any course (current semester)",
            "4. Faculty advisor contact info for a specific student",
            "9. Students advised by a specific lecturer"
        ],
        "Lecturer": [
            "1. Students enrolled in a specific course taught by a particular lecturer",
            "2. Students with average grade above 70% (final year)",
            "4. Faculty advisor contact info for a specific student",
            "5. Lecturers with expertise in a particular area",
            "6. Courses taught by lecturers in a specific department",
            "7. Lecturers who supervised the most research projects",
            "8. Lecturer publications (past year)",
            "9. Students advised by a specific lecturer"
        ],
        "Office Manager - Non Academic": [
            "3. Students not registered in any course (current semester)",
            "4. Faculty advisor contact info for a specific student",
            "8. Lecturer publications (past year)",
            "9. Students advised by a specific lecturer",
            "10. All staff in a specific department"
        ],
        "Administrator": list(get_query_definitions().keys())  # All queries
    }