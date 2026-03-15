# app/db/filters.py


def populate_all_filter_values(app):
    """Populate all filter dropdowns with values from the database.

    :param app: Instance of UniversityDBApp
    """
    if not app.db_manager.cursor:
        return

    # Fetch values from DB (reuse db_manager's fetch_list)
    app.all_departments = app.db_manager.fetch_list(
        "SELECT department_name FROM departments ORDER BY department_name"
    )
    app.all_courses = app.db_manager.fetch_list(
        "SELECT course_name FROM courses ORDER BY course_name"
    )
    app.all_lecturers = app.db_manager.fetch_list(
        "SELECT name FROM lecturers ORDER BY name"
    )
    app.all_students = app.db_manager.fetch_list(
        "SELECT name FROM students ORDER BY name"
    )
    app.all_programs = app.db_manager.fetch_list(
        "SELECT programme_name FROM programmes ORDER BY programme_name"
    )
    app.all_expertise = app.db_manager.fetch_list(
        "SELECT DISTINCT area_name FROM lecturerexpertise ORDER BY area_name"
    )

    # Update filter dropdowns
    app.filter_combo_widgets["department"]["values"] = app.all_departments
    app.filter_combo_widgets["course"]["values"] = app.all_courses
    app.filter_combo_widgets["lecturer"]["values"] = app.all_lecturers
    app.filter_combo_widgets["student"]["values"] = app.all_students
    app.filter_combo_widgets["program"]["values"] = app.all_programs
    app.filter_combo_widgets["expertise"]["values"] = app.all_expertise

    # Reset all filters to "All"
    for key in app.filter_vars:
        app.filter_vars[key].set("All")


def on_department_change(app):
    """Update lecturer/course/program filters when department is selected.

    :param app: Instance of UniversityDBApp
    """
    selected_department = app.filter_vars["department"].get()

    # Reset to all values if "All" is selected
    if selected_department == "All":
        app.filter_combo_widgets["lecturer"]["values"] = app.all_lecturers
        app.filter_combo_widgets["course"]["values"] = app.all_courses
        app.filter_combo_widgets["program"]["values"] = app.all_programs
        return

    # Fetch filtered values from DB
    lecturer_sql = """
        SELECT l.name
        FROM lecturers l
        JOIN departments d ON l.department_id = d.department_id
        WHERE d.department_name = %s
        ORDER BY l.name
    """
    course_sql = """
        SELECT DISTINCT c.course_name
        FROM courses c
        JOIN courselecturers cl ON c.course_code = cl.course_code
        JOIN lecturers l ON cl.lecturer_id = l.lecturer_id
        JOIN departments d ON l.department_id = d.department_id
        WHERE d.department_name = %s
        ORDER BY c.course_name
    """
    program_sql = """
        SELECT p.programme_name
        FROM programmes p
        JOIN departments d ON p.department_id = d.department_id
        WHERE d.department_name = %s
        ORDER BY p.programme_name
    """

    # Update filters
    lecturers = app.db_manager.fetch_list(lecturer_sql, (selected_department,))
    courses = app.db_manager.fetch_list(course_sql, (selected_department,))
    programs = app.db_manager.fetch_list(program_sql, (selected_department,))

    app.filter_combo_widgets["lecturer"]["values"] = lecturers
    app.filter_combo_widgets["course"]["values"] = courses
    app.filter_combo_widgets["program"]["values"] = programs

    # Reset to "All" if current value is no longer valid
    if app.filter_vars["lecturer"].get() not in lecturers:
        app.filter_vars["lecturer"].set("All")
    if app.filter_vars["course"].get() not in courses:
        app.filter_vars["course"].set("All")
    if app.filter_vars["program"].get() not in programs:
        app.filter_vars["program"].set("All")


def on_lecturer_change(app):
    """Update course filter when lecturer is selected.

    :param app: Instance of UniversityDBApp
    """
    selected_lecturer = app.filter_vars["lecturer"].get()

    # Reset to all courses if "All" is selected
    if selected_lecturer == "All":
        app.filter_combo_widgets["course"]["values"] = app.all_courses
        return

    # Fetch filtered courses from DB
    course_sql = """
        SELECT DISTINCT c.course_name
        FROM courses c
        JOIN courselecturers cl ON c.course_code = cl.course_code
        JOIN lecturers l ON cl.lecturer_id = l.lecturer_id
        WHERE l.name = %s
        ORDER BY c.course_name
    """
    courses = app.db_manager.fetch_list(course_sql, (selected_lecturer,))

    # Update course filter
    app.filter_combo_widgets["course"]["values"] = courses

    # Reset to "All" if current course is no longer valid
    if app.filter_vars["course"].get() not in courses:
        app.filter_vars["course"].set("All")