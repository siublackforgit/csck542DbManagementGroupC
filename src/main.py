"""Tkinter GUI for University Database Query Tool (modular, PEP-8 compliant).

This module contains the entire Tkinter interface logic, with:
- Strict PEP-8 compliance (line length, naming, comments)
- Separation of UI setup and business logic
- Descriptive docstrings for all methods
- Input validation and user-friendly error handling
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Import SQL functions from sibling module (PEP-8 relative import)
from src.db_queries import (
    get_students_in_course_by_lecturer,
    get_top_final_year_students,
    get_students_no_current_courses,
    get_student_advisor,
    get_lecturers_by_research_area
)


class UniDBApp(tk.Tk):
    """Main Tkinter application class for the University Database Query Tool.

    Inherits from tk.Tk to create a modular, object-oriented GUI. All methods
    follow PEP-8 standards (snake_case, docstrings, line length).
    """

    def __init__(self):
        """Initialize the main application window and UI elements."""
        super().__init__()

        # Window configuration (PEP-8 line length compliant)
        self.title("University Record Management System")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Initialize UI elements
        self._setup_main_container()
        self._setup_title()
        self._setup_query_selector()
        self._setup_input_frame()
        self._setup_buttons()
        self._setup_results_area()

        # Dynamic input widgets storage (empty dict)
        self.input_widgets = {}
        # Populate initial input fields (default query: 1)
        self.update_input_fields()

    def _setup_main_container(self):
        """Create main container frame for all UI elements."""
        self.main_container = ttk.Frame(self, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)

    def _setup_title(self):
        """Create and position the application title label."""
        title_label = ttk.Label(
            self.main_container,
            text="University Database Query Tool",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

    def _setup_query_selector(self):
        """Create the query selection dropdown menu."""
        # Query selector frame (labeled for clarity)
        query_frame = ttk.LabelFrame(
            self.main_container,
            text="Select Query",
            padding="10"
        )
        query_frame.pack(fill=tk.X, pady=5)

        # Query selection variable and options (PEP-8 line length)
        self.query_selected = tk.StringVar()
        self.query_options = [
            "1. Students in Course (by Lecturer)",
            "2. Final Year Students (Avg Grade >70%)",
            "3. Students with No Current Courses",
            "4. Student's Faculty Advisor",
            "5. Lecturers by Research Area"
        ]

        # Dropdown (combobox) for query selection (readonly to prevent invalid input)
        self.query_dropdown = ttk.Combobox(
            query_frame,
            textvariable=self.query_selected,
            values=self.query_options,
            state="readonly"
        )
        self.query_dropdown.pack(pady=5)
        self.query_dropdown.current(0)  # Default to first query

        # Bind dropdown selection to input field update
        self.query_dropdown.bind(
            "<<ComboboxSelected>>",
            self.update_input_fields
        )

    def _setup_input_frame(self):
        """Create the dynamic input parameters frame."""
        self.input_frame = ttk.LabelFrame(
            self.main_container,
            text="Input Parameters",
            padding="10"
        )
        self.input_frame.pack(fill=tk.X, pady=5)

    def _setup_buttons(self):
        """Create Execute and Clear buttons for query interaction."""
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(fill=tk.X, pady=10)

        # Execute query button
        self.execute_btn = ttk.Button(
            button_frame,
            text="Run Query",
            command=self.run_selected_query
        )
        self.execute_btn.pack(side=tk.LEFT, padx=5)

        # Clear results button
        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear Results",
            command=self.clear_results
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

    def _setup_results_area(self):
        """Create the scrollable text area for displaying query results."""
        result_frame = ttk.LabelFrame(
            self.main_container,
            text="Query Results",
            padding="10"
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrolled text widget (monospace font for aligned results)
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=("Courier New", 10),
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def update_input_fields(self, event=None):
        """Dynamically update input fields based on selected query.

        Clears existing input widgets and creates new ones matching the
        selected query's requirements. Follows PEP-8 for event handling.

        Args:
            event (tk.Event, optional): Combobox selection event. Defaults to None.
        """
        # Clear existing input widgets (PEP-8 loop style)
        for widget in self.input_widgets.values():
            widget.destroy()
        self.input_widgets.clear()

        # Extract query number from selected option (PEP-8 string handling)
        query_number = self.query_selected.get().split(".")[0]

        # Create input fields for each query type
        if query_number == "1":
            # Query 1: Course Code + Lecturer Name
            ttk.Label(
                self.input_frame,
                text="Course Code:"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            course_code_entry = ttk.Entry(self.input_frame, width=20)
            course_code_entry.grid(row=0, column=1, padx=5, pady=5)
            self.input_widgets["course_code"] = course_code_entry

            ttk.Label(
                self.input_frame,
                text="Lecturer Name:"
            ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
            lecturer_name_entry = ttk.Entry(self.input_frame, width=30)
            lecturer_name_entry.grid(row=0, column=3, padx=5, pady=5)
            self.input_widgets["lecturer_name"] = lecturer_name_entry

        elif query_number == "2":
            # Query 2: Minimum Average Grade
            ttk.Label(
                self.input_frame,
                text="Min Avg Grade (%):"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            min_avg_entry = ttk.Entry(self.input_frame, width=10)
            min_avg_entry.insert(0, "70")  # Default value
            min_avg_entry.grid(row=0, column=1, padx=5, pady=5)
            self.input_widgets["min_avg"] = min_avg_entry

        elif query_number == "3":
            # Query 3: Current Semester
            ttk.Label(
                self.input_frame,
                text="Semester (e.g., 2024-1):"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            semester_entry = ttk.Entry(self.input_frame, width=20)
            semester_entry.insert(0, "2024-1")  # Default value
            semester_entry.grid(row=0, column=1, padx=5, pady=5)
            self.input_widgets["semester"] = semester_entry

        elif query_number == "4":
            # Query 4: Student ID
            ttk.Label(
                self.input_frame,
                text="Student ID:"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            student_id_entry = ttk.Entry(self.input_frame, width=10)
            student_id_entry.grid(row=0, column=1, padx=5, pady=5)
            self.input_widgets["student_id"] = student_id_entry

        elif query_number == "5":
            # Query 5: Research Area
            ttk.Label(
                self.input_frame,
                text="Research Area:"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            research_area_entry = ttk.Entry(self.input_frame, width=30)
            research_area_entry.grid(row=0, column=1, padx=5, pady=5)
            self.input_widgets["research_area"] = research_area_entry

    def run_selected_query(self):
        """Execute the selected query, validate inputs, and display results.

        This method:
        1. Clears previous results
        2. Validates user input (non-empty, correct type)
        3. Executes the corresponding SQL query
        4. Passes results to display method
        5. Handles errors with user-friendly messages
        """
        self.clear_results()
        query_number = self.query_selected.get().split(".")[0]
        results = []
        headers = []

        try:
            # Execute query based on selection (PEP-8 conditional structure)
            if query_number == "1":
                # Validate inputs for Query 1
                course_code = self.input_widgets["course_code"].get().strip()
                lecturer_name = self.input_widgets["lecturer_name"].get().strip()

                if not course_code or not lecturer_name:
                    messagebox.showwarning(
                        "Input Error",
                        "Please enter both Course Code and Lecturer Name!"
                    )
                    return

                results = get_students_in_course_by_lecturer(
                    course_code,
                    lecturer_name
                )
                headers = ["Student ID", "Student Name", "Program"]

            elif query_number == "2":
                # Validate inputs for Query 2
                min_avg = self.input_widgets["min_avg"].get().strip()

                if not min_avg.isdigit():
                    messagebox.showwarning(
                        "Input Error",
                        "Minimum Average Grade must be a numeric value!"
                    )
                    return

                results = get_top_final_year_students(int(min_avg))
                headers = ["Student ID", "Name", "Avg Grade (%)", "Program"]

            elif query_number == "3":
                # Validate inputs for Query 3
                semester = self.input_widgets["semester"].get().strip()

                if not semester:
                    messagebox.showwarning(
                        "Input Error",
                        "Please enter a valid semester (e.g., 2024-1)!"
                    )
                    return

                results = get_students_no_current_courses(semester)
                headers = ["Student ID", "Name", "Program"]

            elif query_number == "4":
                # Validate inputs for Query 4
                student_id = self.input_widgets["student_id"].get().strip()

                if not student_id.isdigit():
                    messagebox.showwarning(
                        "Input Error",
                        "Student ID must be a numeric value!"
                    )
                    return

                results = get_student_advisor(int(student_id))
                headers = ["Advisor Name", "Expertise", "Student Contact"]

            elif query_number == "5":
                # Validate inputs for Query 5
                research_area = self.input_widgets["research_area"].get().strip()

                if not research_area:
                    messagebox.showwarning(
                        "Input Error",
                        "Please enter a research area (e.g., AI, Statistics)!"
                    )
                    return

                results = get_lecturers_by_research_area(research_area)
                headers = ["Lecturer ID", "Name", "Department", "Expertise"]

            # Display results (even if empty)
            self.display_results(headers, results)

        except Exception as e:
            # Catch-all error handling (PEP-8 best practice)
            messagebox.showerror(
                "Query Execution Error",
                f"Failed to run query:\n{str(e)}"
            )

    def display_results(self, headers, results):
        """Format and display query results in the scrollable text area.

        Args:
            headers (list): List of column headers for the results
            results (list): List of tuples containing query results
        """
        # Handle empty results (user-friendly message)
        if not results:
            self.result_text.insert(tk.END, "No results found for the query.")
            return

        # Format headers (monospace-aligned with tabs)
        header_line = "\t".join(headers)
        self.result_text.insert(tk.END, header_line + "\n")
        # Add separator line (PEP-8 string manipulation)
        separator = "-" * len(header_line.replace("\t", "    "))
        self.result_text.insert(tk.END, separator + "\n")

        # Format and insert each result row
        for row in results:
            # Replace None with "N/A" for readability (PEP-8 generator expression)
            row_line = "\t".join(
                str(value) if value is not None else "N/A" for value in row
            )
            self.result_text.insert(tk.END, row_line + "\n")

    def clear_results(self):
        """Clear all text from the results display area."""
        self.result_text.delete(1.0, tk.END)


# Run the application (PEP-8 main guard)
if __name__ == "__main__":
    app = UniDBApp()
    app.mainloop()