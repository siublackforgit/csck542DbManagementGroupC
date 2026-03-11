# tests/test_query_execution.py
import unittest
import mysql.connector
from mysql.connector import Error
from app.db.config import DB_CONFIG
from app.db.queries import get_query_definitions

TEST_FILTERS = {
    "department": "Computer Science",
    "course": "Database Systems",
    "lecturer": "Dr. Smith",
    "student": "John Doe",
    "program": "BSc Computer Science",
    "expertise": "Artificial Intelligence"
}

class TestQueryExecution(unittest.TestCase):
    """End-to-end tests for query execution against MySQL database"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests: connect to MySQL"""
        try:
            # Connect to the database
            cls.connection = mysql.connector.connect(**DB_CONFIG)
            cls.cursor = cls.connection.cursor(dictionary=True)   
            cls.queries = get_query_definitions()
            print(f"✅ Connected to MySQL database: {DB_CONFIG['database']}")
        except Error as e:
            raise RuntimeError(f"Failed to connect to MySQL: {e}") from e

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests: close connection"""
        if cls.connection.is_connected():
            cls.cursor.close()
            cls.connection.close()
            print("✅ MySQL connection closed")

    def test_all_queries_execute_without_error(self):
        """Test every query runs without SQL errors (returns valid cursor)"""
        for query_name, query_data in self.queries.items():
            with self.subTest(query_name=query_name):
                try:
                    sql = query_data["sql"].strip()
                    params = query_data["params"](TEST_FILTERS)
                    
                    # Execute query
                    self.cursor.execute(sql, params)
                    
                    # Verify cursor is valid (no execution error)
                    self.assertTrue(self.cursor._executed, f"Query '{query_name}' failed to execute")
                    print(f"Query executed: {query_name}")
                except Error as e:
                    self.fail(f" Query '{query_name}' failed with error: {e}\nSQL: {sql}\nParams: {params}")

    def test_query_1_student_enrollment(self):
        """Test Query 1: Students in course taught by lecturer"""
        query = self.queries["1. Students enrolled in a specific course taught by a particular lecturer"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        # Validate result structure (columns exist)
        if results:
            self.assertIn("student_id", results[0])
            self.assertIn("student_name", results[0])
            self.assertIn("course_name", results[0])
            self.assertIn("lecturer_name", results[0])

    def test_query_2_average_grade_70_plus(self):
        """Test Query 2: Final-year students with avg grade >70%"""
        query = self.queries["2. Students with average grade above 70% (final year)"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        # Validate average grade is >70 (if results exist)
        for row in results:
            if row["average_grade"]:
                self.assertGreater(row["average_grade"], 70, f"Invalid grade: {row['average_grade']}")

    def test_query_3_unregistered_students(self):
        """Test Query 3: Students with no course registration"""
        query = self.queries["3. Students not registered in any course (current semester)"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        # Validate result structure
        if results:
            self.assertIn("student_id", results[0])
            self.assertIn("name", results[0])
            self.assertIn("programme_name", results[0])

    def test_query_4_advisor_contact(self):
        """Test Query 4: Faculty advisor info for student"""
        query = self.queries["4. Faculty advisor contact info for a specific student"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        # Validate advisor info exists (if results exist)
        if results:
            self.assertIn("student_name", results[0])
            self.assertIn("advisor_name", results[0])
            self.assertIn("department_name", results[0])

    def test_query_5_lecturer_expertise(self):
        """Test Query 5: Lecturers with specific expertise"""
        query = self.queries["5. Lecturers with expertise in a particular research area"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        # Validate expertise area matches (if results exist)
        for row in results:
            if row["expertise_area"]:
                self.assertEqual(
                    row["expertise_area"], TEST_FILTERS["expertise"],
                    f"Expected expertise: {TEST_FILTERS['expertise']}, got: {row['expertise_area']}"
                )

    def test_query_6_courses_by_department(self):
        """Test Query 6: Courses taught in specific department"""
        query = self.queries["6. Courses taught by lecturers in a specific department"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        for row in results:
            if row["department_name"]:
                self.assertEqual(
                    row["department_name"], TEST_FILTERS["department"],
                    f"Expected department: {TEST_FILTERS['department']}, got: {row['department_name']}"
                )

    def test_query_7_top_research_supervisors(self):
        """Test Query 7: Lecturers with most research projects"""
        query = self.queries["7. Lecturers who supervised the most research projects"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        if results:
            self.assertIn("lecturer_name", results[0])
            self.assertIn("total_projects", results[0])

    def test_query_8_lecturer_publications(self):
        """Test Query 8: Lecturer publications (past year)"""
        query = self.queries["8. Lecturer publications (past year)"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        from datetime import datetime, timedelta
        one_year_ago = datetime.now() - timedelta(days=365)
        
        for row in results:
            if row["publication_date"]:
                pub_date = row["publication_date"]
                self.assertGreaterEqual(pub_date, one_year_ago.date(), 
                                       f"Publication date {pub_date} is older than 1 year")

    def test_query_9_students_advised_by_lecturer(self):
        """Test Query 9: Students advised by specific lecturer"""
        query = self.queries["9. Students advised by a specific lecturer"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        for row in results:
            if row["advisor_name"]:
                self.assertEqual(
                    row["advisor_name"], TEST_FILTERS["lecturer"],
                    f"Expected lecturer: {TEST_FILTERS['lecturer']}, got: {row['advisor_name']}"
                )

    def test_query_10_staff_in_department(self):
        """Test Query 10: Staff in specific department"""
        query = self.queries["10. All staff in a specific department"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        for row in results:
            if row["department_name"]:
                self.assertEqual(
                    row["department_name"], TEST_FILTERS["department"],
                    f"Expected department: {TEST_FILTERS['department']}, got: {row['department_name']}"
                )

    def test_query_11_student_supervisors(self):
        """Test Query 11: Employees supervising students in program"""
        query = self.queries["11. Employees supervising student employees in a particular program"]
        sql = query["sql"].strip()
        params = query["params"](TEST_FILTERS)
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        for row in results:
            if row["programme_name"]:
                self.assertEqual(
                    row["programme_name"], TEST_FILTERS["program"],
                    f"Expected program: {TEST_FILTERS['program']}, got: {row['programme_name']}"
                )

if __name__ == "__main__":
    unittest.main(verbosity=2)