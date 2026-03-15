import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

from app.db.config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            return True, "Connected to MySQL database successfully."
        except Error as e:
            return False, f"Could not connect to MySQL.\n\n{e}"

    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def fetch_list(self, sql, params=()):
        """Fetch a list of values for filter dropdowns."""
        if not self.cursor:
            return ["All"]
        try:
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            return ["All"] + [
                list(row.values())[0] for row in rows if list(row.values())[0] is not None
            ]
        except Error as e:
            messagebox.showerror("Query Error", f"Failed to load filter values.\n\n{e}")
            return ["All"]

    def run_query(self, sql, params=()):
        """Execute a raw SQL query and return results."""
        if not self.cursor:
            return None, "No active database connection."
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall(), "Query executed successfully."
        except Error as e:
            return None, f"An error occurred while running the query.\n\n{e}"