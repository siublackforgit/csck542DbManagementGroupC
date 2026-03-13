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
    @classmethod
    def setUpClass(cls):
        cls.connection = mysql.connector.connect(**DB_CONFIG)
        cls.cursor = cls.connection.cursor(dictionary=True)
        cls.queries = get_query_definitions()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.cursor.close()
            cls.connection.close()
        except:
            pass

    def test_all_11_queries_execute_successfully(self):
        for query_name, query_data in self.queries.items():
            with self.subTest(query=query_name):
                try:
                    sql = query_data["sql"]
                    params = query_data["params"](TEST_FILTERS)

                    self.cursor.execute(sql, params)
                    self.cursor.fetchall()  # 🔥 修复核心：必须读结果

                    print(f"✅ {query_name}")
                except Exception as e:
                    self.fail(f"❌ {query_name} -> {str(e)}")

if __name__ == "__main__":
    unittest.main(verbosity=2)