import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error


class UniversityDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Database Management and Query System")
        self.root.geometry("1550x930")
        self.root.minsize(1320, 800)

        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "YOUR PASSWORD",
            "database": "YOUR DATABASE_db"
        }

        self.conn = None
        self.cursor = None
        self.style = ttk.Style()

        self.filter_vars = {
            "department": tk.StringVar(value="All"),
            "course": tk.StringVar(value="All"),
            "lecturer": tk.StringVar(value="All"),
            "student": tk.StringVar(value="All"),
            "program": tk.StringVar(value="All"),
            "expertise": tk.StringVar(value="All")
        }

        self.query_var = tk.StringVar()
        self.role_var = tk.StringVar(value="Student")
        self.status_var = tk.StringVar(value="Ready")
        self.result_count_var = tk.StringVar(value="Rows: 0")

        self.filter_combo_widgets = {}
        self.filter_frames = {}
        self.current_rows = []
        self.sort_states = {}

        self.icon_refs = {}
        self.header_icon = None
        self.run_icon = None
        self.clear_icon = None
        self.refresh_icon = None

        self.configure_styles()
        self.load_icons()

        self.QUERY_DEFINITIONS = self.build_query_definitions()
        self.ROLE_PERMISSIONS = self.build_role_permissions()

        self.build_layout()
        self.connect_to_database()
        self.populate_all_filter_values()
        self.on_role_change()

    def configure_styles(self):
        self.colors = {
            "bg_main": "#eef3f8",
            "bg_card": "#ffffff",
            "bg_header": "#0f2742",
            "text_dark": "#1f2937",
            "text_light": "#ffffff",
            "muted_text": "#d9e6f2",
            "border": "#cbd5e1",
            "table_header": "#dbeafe",
            "selected": "#bfdbfe",
            "status_bg": "#dbeafe",
            "info_bg": "#f8fafc",
            "info_body": "#334155",
            "button_run": "#0b63a5",
            "button_run_hover": "#084c7d",
            "button_clear": "#4b5563",
            "button_clear_hover": "#374151",
            "button_refresh": "#7c3aed",
            "button_refresh_hover": "#5b21b6",
            "button_export": "#8a5a00",
            "button_export_hover": "#6b4500",
            "button_text": "#ffffff",
            "hover_outline": "#0b63a5",
            "control_bg": "#ffffff",
            "control_hover_bg": "#eef6ff"
        }

        self.root.configure(bg=self.colors["bg_main"])
        self.style.theme_use("clam")

        self.style.configure("Card.TFrame", background=self.colors["bg_card"])

        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold"),
            background=self.colors["bg_header"],
            foreground=self.colors["text_light"],
            padding=(6, 4)
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10),
            background=self.colors["bg_header"],
            foreground=self.colors["muted_text"],
            padding=(6, 0, 6, 4)
        )

        self.style.configure(
            "Section.TLabelframe",
            background=self.colors["bg_card"],
            borderwidth=1,
            relief="solid"
        )

        self.style.configure(
            "Section.TLabelframe.Label",
            background=self.colors["bg_card"],
            foreground=self.colors["text_dark"],
            font=("Segoe UI", 11, "bold")
        )

        self.style.configure(
            "TLabel",
            background=self.colors["bg_card"],
            foreground=self.colors["text_dark"],
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "PanelValue.TLabel",
            background=self.colors["bg_card"],
            foreground=self.colors["button_run"],
            font=("Segoe UI", 11, "bold")
        )

        self.style.configure(
            "Accessible.TCombobox",
            padding=5,
            font=("Segoe UI", 10),
            arrowsize=16
        )

        self.style.map(
            "Accessible.TCombobox",
            fieldbackground=[
                ("readonly", self.colors["control_bg"]),
                ("focus", self.colors["control_hover_bg"])
            ],
            selectbackground=[
                ("readonly", self.colors["control_bg"])
            ],
            selectforeground=[
                ("readonly", self.colors["text_dark"])
            ],
            foreground=[
                ("readonly", self.colors["text_dark"])
            ]
        )

        self.style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background="white",
            fieldbackground="white",
            foreground=self.colors["text_dark"],
            bordercolor=self.colors["border"],
            borderwidth=1
        )

        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.colors["table_header"],
            foreground=self.colors["text_dark"],
            relief="flat",
            padding=8
        )

        self.style.map(
            "Treeview",
            background=[("selected", self.colors["selected"])],
            foreground=[("selected", self.colors["text_dark"])]
        )

    def load_icons(self):
        self.header_icon = self.load_single_icon(
            ["University_Icon.png", "Univeristy_Icon.png"],
            subsample=(6, 6)
        )
        self.run_icon = self.load_single_icon(
            ["Run Query.png", "Run_Query.png", "run_query.png"],
            subsample=(14, 14)
        )
        self.clear_icon = self.load_single_icon(
            ["Clear Results.png", "Clear_Results.png", "clear_results.png"],
            subsample=(14, 14)
        )
        self.refresh_icon = self.load_single_icon(
            ["Refresh.png", "refresh.png"],
            subsample=(14, 14)
        )

    def load_single_icon(self, possible_names, subsample=(1, 1)):
        search_paths = []

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            search_paths.extend([
                base_dir,
                os.path.join(base_dir, "assets")
            ])
        except Exception:
            pass

        search_paths.extend([
            os.getcwd(),
            "/mnt/data"
        ])

        for folder in search_paths:
            for name in possible_names:
                full_path = os.path.join(folder, name)
                if os.path.exists(full_path):
                    try:
                        img = tk.PhotoImage(file=full_path)
                        sx, sy = subsample
                        if sx > 1 or sy > 1:
                            img = img.subsample(sx, sy)
                        self.icon_refs[full_path] = img
                        return img
                    except Exception:
                        continue
        return None

    def build_layout(self):
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header_bg = tk.Frame(self.root, bg=self.colors["bg_header"], height=78)
        header_bg.grid(row=0, column=0, sticky="ew")
        header_bg.grid_propagate(False)

        header_inner = tk.Frame(header_bg, bg=self.colors["bg_header"])
        header_inner.pack(expand=True, fill="both")

        title_container = tk.Frame(header_inner, bg=self.colors["bg_header"])
        title_container.pack(pady=(6, 0))

        if self.header_icon:
            icon_label = tk.Label(
                title_container,
                image=self.header_icon,
                bg=self.colors["bg_header"],
                bd=0
            )
            icon_label.pack(side="left", padx=(0, 12))

        title_label = ttk.Label(
            title_container,
            text="University Database Management and Query System",
            style="Title.TLabel",
            anchor="center"
        )
        title_label.pack(side="left")

        subtitle_label = ttk.Label(
            header_inner,
            text="Role based academic information access for Students, Lecturers, Office Managers, and Administrators",
            style="Subtitle.TLabel",
            anchor="center"
        )
        subtitle_label.pack()

        dashboard_frame = ttk.Frame(self.root, style="Card.TFrame")
        dashboard_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(10, 8))

        for i in range(3):
            dashboard_frame.grid_columnconfigure(i, weight=1, uniform="dash")

        self.build_role_filters_dashboard(dashboard_frame)
        self.build_query_dashboard(dashboard_frame)
        self.build_project_info_dashboard(dashboard_frame)

        action_frame = ttk.Frame(self.root, style="Card.TFrame")
        action_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 8))

        self.run_button = self.create_accessible_button(
            parent=action_frame,
            text="Run Query",
            icon=self.run_icon,
            bg=self.colors["button_run"],
            hover_bg=self.colors["button_run_hover"],
            command=self.run_selected_query
        )
        self.run_button.pack(side="left", padx=(0, 10))

        self.clear_button = self.create_accessible_button(
            parent=action_frame,
            text="Clear Results",
            icon=self.clear_icon,
            bg=self.colors["button_clear"],
            hover_bg=self.colors["button_clear_hover"],
            command=self.clear_results
        )
        self.clear_button.pack(side="left", padx=(0, 10))

        self.refresh_button = self.create_accessible_button(
            parent=action_frame,
            text="Refresh Filters",
            icon=self.refresh_icon,
            bg=self.colors["button_refresh"],
            hover_bg=self.colors["button_refresh_hover"],
            command=self.refresh_filters
        )
        self.refresh_button.pack(side="left", padx=(0, 10))

        self.export_button = self.create_accessible_button(
            parent=action_frame,
            text="Export CSV",
            icon=None,
            bg=self.colors["button_export"],
            hover_bg=self.colors["button_export_hover"],
            command=self.export_results_to_csv
        )
        self.export_button.pack(side="left", padx=(0, 10))

        ttk.Label(
            action_frame,
            textvariable=self.result_count_var,
            style="PanelValue.TLabel"
        ).pack(side="right", padx=(10, 0))

        self.build_results_section()

        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            bg=self.colors["status_bg"],
            fg=self.colors["text_dark"],
            font=("Segoe UI", 10),
            padx=10,
            pady=8
        )
        status_bar.grid(row=4, column=0, sticky="ew")

    def create_accessible_button(self, parent, text, icon, bg, hover_bg, command):
        btn = tk.Button(
            parent,
            text=text,
            image=icon,
            compound="left",
            command=command,
            bg=bg,
            activebackground=hover_bg,
            fg=self.colors["button_text"],
            activeforeground=self.colors["button_text"],
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
            bd=0,
            relief="flat",
            cursor="hand2"
        )
        btn.default_bg = bg
        btn.hover_bg = hover_bg
        btn.bind("<Enter>", lambda event, b=btn: self.on_button_hover_in(b))
        btn.bind("<Leave>", lambda event, b=btn: self.on_button_hover_out(b))
        return btn

    def on_button_hover_in(self, button):
        button.configure(bg=button.hover_bg)

    def on_button_hover_out(self, button):
        button.configure(bg=button.default_bg)

    def build_role_filters_dashboard(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="1. Role Access and Dynamic Filters",
            style="Section.TLabelframe"
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        frame.grid_columnconfigure(0, weight=1)

        current_row = 0

        ttk.Label(frame, text="Select Role:").grid(
            row=current_row, column=0, sticky="w", padx=10, pady=(8, 2)
        )
        current_row += 1

        role_wrapper = self.create_hoverable_control_wrapper(frame)
        role_wrapper.grid(row=current_row, column=0, sticky="ew", padx=10, pady=(0, 6))

        self.role_combo = ttk.Combobox(
            role_wrapper,
            textvariable=self.role_var,
            values=["Student", "Lecturer", "Office Manager - Non Academic", "Administrator"],
            state="readonly",
            style="Accessible.TCombobox"
        )
        self.role_combo.pack(fill="x")
        self.role_combo.bind("<<ComboboxSelected>>", lambda event: self.on_role_change())
        self.bind_control_hover(role_wrapper, self.role_combo)
        current_row += 1

        ttk.Label(frame, text="Current Access Level:").grid(
            row=current_row, column=0, sticky="w", padx=10, pady=(0, 2)
        )
        current_row += 1

        self.role_info_label = ttk.Label(frame, text="Student", style="PanelValue.TLabel")
        self.role_info_label.grid(
            row=current_row, column=0, sticky="w", padx=10, pady=(0, 8)
        )
        current_row += 1

        filter_order = [
            ("Department:", "department"),
            ("Course:", "course"),
            ("Lecturer:", "lecturer"),
            ("Student:", "student"),
            ("Program:", "program"),
            ("Expertise:", "expertise"),
        ]

        for label_text, key in filter_order:
            container = ttk.Frame(frame, style="Card.TFrame")
            container.grid(row=current_row, column=0, sticky="ew", padx=10, pady=(0, 6))
            container.grid_columnconfigure(0, weight=1)

            label = ttk.Label(container, text=label_text)
            label.grid(row=0, column=0, sticky="w", pady=(0, 2))

            combo_wrapper = self.create_hoverable_control_wrapper(container)
            combo_wrapper.grid(row=1, column=0, sticky="ew")

            combo = ttk.Combobox(
                combo_wrapper,
                textvariable=self.filter_vars[key],
                state="readonly",
                style="Accessible.TCombobox"
            )
            combo.pack(fill="x")

            self.filter_frames[key] = container
            self.filter_combo_widgets[key] = combo
            self.bind_control_hover(combo_wrapper, combo)

            current_row += 1

        self.filter_combo_widgets["department"].bind(
            "<<ComboboxSelected>>",
            lambda event: self.on_department_change()
        )
        self.filter_combo_widgets["lecturer"].bind(
            "<<ComboboxSelected>>",
            lambda event: self.on_lecturer_change()
        )

    def build_query_dashboard(self, parent):
        frame = ttk.LabelFrame(parent, text="2. Query Selection and Description", style="Section.TLabelframe")
        frame.grid(row=0, column=1, sticky="nsew", padx=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        ttk.Label(frame, text="Choose Query:").grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))

        query_wrapper = self.create_hoverable_control_wrapper(frame)
        query_wrapper.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))

        self.query_combo = ttk.Combobox(
            query_wrapper,
            textvariable=self.query_var,
            state="readonly",
            style="Accessible.TCombobox"
        )
        self.query_combo.pack(fill="x")
        self.query_combo.bind("<<ComboboxSelected>>", lambda event: self.on_query_change())
        self.bind_control_hover(query_wrapper, self.query_combo)

        ttk.Label(frame, text="Query Description:").grid(row=2, column=0, sticky="w", padx=10, pady=(0, 2))

        self.query_description = tk.Text(
            frame,
            height=7,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg="#334155",
            relief="solid",
            bd=1
        )
        self.query_description.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.query_description.config(state="disabled")

    def build_project_info_dashboard(self, parent):
        frame = ttk.LabelFrame(parent, text="3. Project Information", style="Section.TLabelframe")
        frame.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        info_text = tk.Text(
            frame,
            height=7,
            wrap="word",
            font=("Segoe UI", 10),
            bg=self.colors["info_bg"],
            fg=self.colors["info_body"],
            relief="solid",
            bd=1
        )
        info_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        project_description = (
            "Project Overview:\n"
            "This system manages and queries academic data through a structured role based interface.\n\n"

            "Mini Dashboards\n"
            "1. Role Access and Dynamic Filters\n"
            "2. Query Selection and Description\n"
            "3. Project Information\n\n"

            "Project Team:\n"
            "Jessica Cardile\n"
            "Malarvizhi Madhaiyan\n"
            "Ka Chun Yeung\n"
            "Jorg Alexander Reiff Nothacker\n"
            "Mazen Al Adhami"
        )

        info_text.insert("1.0", project_description)
        info_text.config(state="disabled")

    def create_hoverable_control_wrapper(self, parent):
        wrapper = tk.Frame(
            parent,
            bg=self.colors["border"],
            highlightthickness=2,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["hover_outline"],
            bd=0
        )
        return wrapper

    def bind_control_hover(self, wrapper, widget):
        def hover_in(event=None):
            wrapper.config(highlightbackground=self.colors["hover_outline"], bg=self.colors["hover_outline"])

        def hover_out(event=None):
            wrapper.config(highlightbackground=self.colors["border"], bg=self.colors["border"])

        wrapper.bind("<Enter>", hover_in)
        wrapper.bind("<Leave>", hover_out)
        widget.bind("<Enter>", hover_in)
        widget.bind("<Leave>", hover_out)
        widget.bind("<FocusIn>", hover_in)
        widget.bind("<FocusOut>", hover_out)

    def build_results_section(self):
        result_frame = ttk.LabelFrame(self.root, text="Query Results", style="Section.TLabelframe")
        result_frame.grid(row=3, column=0, sticky="nsew", padx=18, pady=(0, 14))
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        tree_container = ttk.Frame(result_frame, style="Card.TFrame")
        tree_container.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        self.result_tree = ttk.Treeview(tree_container, show="headings")
        self.result_tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.result_tree.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")

        x_scroll = ttk.Scrollbar(tree_container, orient="horizontal", command=self.result_tree.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.result_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.result_tree.tag_configure("oddrow", background="#f8fafc")
        self.result_tree.tag_configure("evenrow", background="#ffffff")

    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor(dictionary=True)
            self.status_var.set("Connected to MySQL database successfully.")
        except Error as e:
            self.status_var.set("Database connection failed.")
            messagebox.showerror("Database Connection Error", f"Could not connect to MySQL.\n\n{e}")

    def build_query_definitions(self):
        return {
            "1. Students enrolled in a specific course taught by a particular lecturer": {
                "description": "Returns students enrolled in the chosen course where the offering is linked to the selected lecturer.",
                "filters": ["course", "lecturer"],
                "sql": """
                    SELECT
                        s.student_id,
                        s.full_name AS student_name,
                        c.course_code,
                        c.course_name,
                        l.full_name AS lecturer_name
                    FROM students s
                    JOIN enrollments e ON s.student_id = e.student_id
                    JOIN course_offerings co ON e.offering_id = co.offering_id
                    JOIN courses c ON co.course_code = c.course_code
                    JOIN offering_lecturers ol ON co.offering_id = ol.offering_id
                    JOIN lecturers l ON ol.lecturer_id = l.lecturer_id
                    WHERE (%s = 'All' OR c.course_name = %s)
                      AND (%s = 'All' OR l.full_name = %s)
                    ORDER BY s.full_name;
                """,
                "params": lambda f: (f["course"], f["course"], f["lecturer"], f["lecturer"])
            },

            "2. Students with average grade above 70": {
                "description": "Lists students whose average numeric grade is above 70.",
                "filters": ["program"],
                "sql": """
                    SELECT
                        s.student_id,
                        s.full_name,
                        p.program_name,
                        ROUND(AVG(e.numeric_grade), 2) AS average_grade
                    FROM students s
                    LEFT JOIN programs p ON s.program_id = p.program_id
                    JOIN enrollments e ON s.student_id = e.student_id
                    WHERE (%s = 'All' OR p.program_name = %s)
                      AND e.numeric_grade IS NOT NULL
                    GROUP BY s.student_id, s.full_name, p.program_name
                    HAVING AVG(e.numeric_grade) > 70
                    ORDER BY average_grade DESC, s.full_name;
                """,
                "params": lambda f: (f["program"], f["program"])
            },

            "3. Students not registered in any course offering": {
                "description": "Finds students who do not have any enrollment record.",
                "filters": ["program"],
                "sql": """
                    SELECT
                        s.student_id,
                        s.full_name,
                        s.email,
                        p.program_name
                    FROM students s
                    LEFT JOIN programs p ON s.program_id = p.program_id
                    WHERE (%s = 'All' OR p.program_name = %s)
                      AND s.student_id NOT IN (
                          SELECT DISTINCT student_id
                          FROM enrollments
                      )
                    ORDER BY s.full_name;
                """,
                "params": lambda f: (f["program"], f["program"])
            },

            "4. Faculty advisor contact information for a specific student": {
                "description": "Returns advisor details using the student_advisors table.",
                "filters": ["student"],
                "sql": """
                    SELECT
                        s.full_name AS student_name,
                        l.full_name AS advisor_name,
                        d.department_name
                    FROM student_advisors sa
                    JOIN students s ON sa.student_id = s.student_id
                    JOIN lecturers l ON sa.lecturer_id = l.lecturer_id
                    LEFT JOIN departments d ON l.department_id = d.department_id
                    WHERE (%s = 'All' OR s.full_name = %s)
                    ORDER BY s.full_name;
                """,
                "params": lambda f: (f["student"], f["student"])
            },

            "5. Lecturers with expertise in a particular area": {
                "description": "Lists lecturers whose expertise matches the selected value.",
                "filters": ["expertise"],
                "sql": """
                    SELECT
                        l.lecturer_id,
                        l.full_name,
                        le.expertise_area
                    FROM lecturers l
                    JOIN lecturer_expertise le ON l.lecturer_id = le.lecturer_id
                    WHERE (%s = 'All' OR le.expertise_area = %s)
                    ORDER BY l.full_name;
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
                        l.full_name AS lecturer_name,
                        d.department_name
                    FROM courses c
                    JOIN course_offerings co ON co.course_code = c.course_code
                    JOIN offering_lecturers ol ON co.offering_id = ol.offering_id
                    JOIN lecturers l ON ol.lecturer_id = l.lecturer_id
                    JOIN departments d ON l.department_id = d.department_id
                    WHERE (%s = 'All' OR d.department_name = %s)
                    ORDER BY c.course_name;
                """,
                "params": lambda f: (f["department"], f["department"])
            },

            "7. Lecturers who supervised the most research projects": {
                "description": "Ranks lecturers by the number of research projects led by each lecturer.",
                "filters": [],
                "sql": """
                    SELECT
                        l.lecturer_id,
                        l.full_name AS lecturer_name,
                        COUNT(rp.project_id) AS total_projects
                    FROM lecturers l
                    LEFT JOIN research_projects rp
                        ON l.lecturer_id = rp.principal_investigator_id
                    GROUP BY l.lecturer_id, l.full_name
                    ORDER BY total_projects DESC, l.full_name;
                """,
                "params": lambda f: ()
            },

            "8. Publications of lecturers": {
                "description": "Shows publications for lecturers.",
                "filters": ["lecturer"],
                "sql": """
                    SELECT
                        l.full_name AS lecturer_name,
                        p.title AS publication_title,
                        p.publication_date
                    FROM publications p
                    JOIN lecturers l ON p.lecturer_id = l.lecturer_id
                    WHERE (%s = 'All' OR l.full_name = %s)
                    ORDER BY p.publication_date DESC;
                """,
                "params": lambda f: (f["lecturer"], f["lecturer"])
            },

            "9. Students advised by a specific lecturer": {
                "description": "Lists students supervised or advised by the selected lecturer.",
                "filters": ["lecturer"],
                "sql": """
                    SELECT
                        l.full_name AS advisor_name,
                        s.student_id,
                        s.full_name AS student_name,
                        s.email
                    FROM student_advisors sa
                    JOIN lecturers l ON sa.lecturer_id = l.lecturer_id
                    JOIN students s ON sa.student_id = s.student_id
                    WHERE (%s = 'All' OR l.full_name = %s)
                    ORDER BY s.full_name;
                """,
                "params": lambda f: (f["lecturer"], f["lecturer"])
            },

            "10. All students in a selected department": {
                "description": "Lists all students belonging to programs under the selected department.",
                "filters": ["department"],
                "sql": """
                    SELECT
                        s.student_id,
                        s.full_name,
                        s.email,
                        d.department_name,
                        p.program_name
                    FROM students s
                    LEFT JOIN programs p ON s.program_id = p.program_id
                    LEFT JOIN departments d ON p.department_id = d.department_id
                    WHERE (%s = 'All' OR d.department_name = %s)
                    ORDER BY s.full_name;
                """,
                "params": lambda f: (f["department"], f["department"])
            },

            "11. Course offerings by semester and department": {
                "description": "Returns course offerings filtered by department.",
                "filters": ["department"],
                "sql": """
                    SELECT
                        co.offering_id,
                        c.course_code,
                        c.course_name,
                        co.semester,
                        co.schedule_text,
                        co.room,
                        d.department_name
                    FROM course_offerings co
                    JOIN courses c ON co.course_code = c.course_code
                    LEFT JOIN departments d ON c.department_id = d.department_id
                    WHERE (%s = 'All' OR d.department_name = %s)
                    ORDER BY co.semester, c.course_name;
                """,
                "params": lambda f: (f["department"], f["department"])
            }
        }

    def build_role_permissions(self):
        return {
            "Student": [
                "1. Students enrolled in a specific course taught by a particular lecturer",
                "3. Students not registered in any course offering",
                "4. Faculty advisor contact information for a specific student",
                "9. Students advised by a specific lecturer"
            ],
            "Lecturer": [
                "1. Students enrolled in a specific course taught by a particular lecturer",
                "2. Students with average grade above 70",
                "4. Faculty advisor contact information for a specific student",
                "5. Lecturers with expertise in a particular area",
                "6. Courses taught by lecturers in a specific department",
                "7. Lecturers who supervised the most research projects",
                "8. Publications of lecturers",
                "9. Students advised by a specific lecturer"
            ],
            "Office Manager - Non Academic": [
                "3. Students not registered in any course offering",
                "4. Faculty advisor contact information for a specific student",
                "8. Publications of lecturers",
                "9. Students advised by a specific lecturer",
                "10. All students in a selected department"
            ],
            "Administrator": list(self.QUERY_DEFINITIONS.keys())
        }

    def fetch_list(self, sql, params=()):
        try:
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            return ["All"] + [list(row.values())[0] for row in rows if list(row.values())[0] is not None]
        except Error as e:
            messagebox.showerror("Query Error", f"Failed to load filter values.\n\n{e}")
            return ["All"]

    def populate_all_filter_values(self):
        if not self.cursor:
            return

        self.all_departments = self.fetch_list(
            "SELECT department_name FROM departments ORDER BY department_name"
        )
        self.all_courses = self.fetch_list(
            "SELECT course_name FROM courses ORDER BY course_name"
        )
        self.all_lecturers = self.fetch_list(
            "SELECT full_name FROM lecturers ORDER BY full_name"
        )
        self.all_students = self.fetch_list(
            "SELECT full_name FROM students ORDER BY full_name"
        )
        self.all_programs = self.fetch_list(
            "SELECT program_name FROM programs ORDER BY program_name"
        )
        self.all_expertise = self.fetch_list(
            "SELECT DISTINCT expertise_area FROM lecturer_expertise ORDER BY expertise_area"
        )

        self.filter_combo_widgets["department"]["values"] = self.all_departments
        self.filter_combo_widgets["course"]["values"] = self.all_courses
        self.filter_combo_widgets["lecturer"]["values"] = self.all_lecturers
        self.filter_combo_widgets["student"]["values"] = self.all_students
        self.filter_combo_widgets["program"]["values"] = self.all_programs
        self.filter_combo_widgets["expertise"]["values"] = self.all_expertise

        for key in self.filter_vars:
            self.filter_vars[key].set("All")

    def refresh_filters(self):
        self.populate_all_filter_values()
        self.on_query_change()
        self.status_var.set("Filters refreshed from database.")

    def on_role_change(self):
        selected_role = self.role_var.get()
        allowed_queries = self.ROLE_PERMISSIONS.get(selected_role, [])

        self.role_info_label.config(text=selected_role)
        self.query_combo["values"] = allowed_queries

        if allowed_queries:
            self.query_var.set(allowed_queries[0])
            self.on_query_change()
            self.status_var.set(f"Role changed to {selected_role}. Available queries updated.")
        else:
            self.query_var.set("")
            self.query_description.config(state="normal")
            self.query_description.delete("1.0", tk.END)
            self.query_description.config(state="disabled")
            self.status_var.set(f"No queries available for role: {selected_role}")

    def on_query_change(self):
        selected_query = self.query_var.get()
        query_info = self.QUERY_DEFINITIONS.get(selected_query)

        if not query_info:
            return

        self.query_description.config(state="normal")
        self.query_description.delete("1.0", tk.END)
        self.query_description.insert(tk.END, query_info["description"])
        self.query_description.config(state="disabled")

        active_filters = query_info["filters"]

        for key, frame in self.filter_frames.items():
            if key in active_filters:
                frame.grid()
            else:
                frame.grid_remove()

        self.status_var.set(f"Selected query: {selected_query}")

    def on_department_change(self):
        selected_department = self.filter_vars["department"].get()

        if selected_department == "All":
            self.filter_combo_widgets["lecturer"]["values"] = self.all_lecturers
            self.filter_combo_widgets["course"]["values"] = self.all_courses
            self.filter_combo_widgets["program"]["values"] = self.all_programs
            return

        lecturer_sql = """
            SELECT l.full_name
            FROM lecturers l
            JOIN departments d ON l.department_id = d.department_id
            WHERE d.department_name = %s
            ORDER BY l.full_name
        """

        course_sql = """
            SELECT DISTINCT c.course_name
            FROM courses c
            JOIN course_offerings co ON co.course_code = c.course_code
            JOIN offering_lecturers ol ON co.offering_id = ol.offering_id
            JOIN lecturers l ON ol.lecturer_id = l.lecturer_id
            JOIN departments d ON l.department_id = d.department_id
            WHERE d.department_name = %s
            ORDER BY c.course_name
        """

        program_sql = """
            SELECT p.program_name
            FROM programs p
            JOIN departments d ON p.department_id = d.department_id
            WHERE d.department_name = %s
            ORDER BY p.program_name
        """

        lecturers = self.fetch_list(lecturer_sql, (selected_department,))
        courses = self.fetch_list(course_sql, (selected_department,))
        programs = self.fetch_list(program_sql, (selected_department,))

        self.filter_combo_widgets["lecturer"]["values"] = lecturers
        self.filter_combo_widgets["course"]["values"] = courses
        self.filter_combo_widgets["program"]["values"] = programs

        if self.filter_vars["lecturer"].get() not in lecturers:
            self.filter_vars["lecturer"].set("All")
        if self.filter_vars["course"].get() not in courses:
            self.filter_vars["course"].set("All")
        if self.filter_vars["program"].get() not in programs:
            self.filter_vars["program"].set("All")

    def on_lecturer_change(self):
        selected_lecturer = self.filter_vars["lecturer"].get()

        if selected_lecturer == "All":
            self.filter_combo_widgets["course"]["values"] = self.all_courses
            return

        course_sql = """
            SELECT DISTINCT c.course_name
            FROM courses c
            JOIN course_offerings co ON co.course_code = c.course_code
            JOIN offering_lecturers ol ON co.offering_id = ol.offering_id
            JOIN lecturers l ON ol.lecturer_id = l.lecturer_id
            WHERE l.full_name = %s
            ORDER BY c.course_name
        """

        courses = self.fetch_list(course_sql, (selected_lecturer,))
        self.filter_combo_widgets["course"]["values"] = courses

        if self.filter_vars["course"].get() not in courses:
            self.filter_vars["course"].set("All")

    def run_selected_query(self):
        if not self.cursor:
            messagebox.showwarning("No Connection", "No active database connection.")
            return

        selected_role = self.role_var.get()
        selected_query = self.query_var.get()

        allowed_queries = self.ROLE_PERMISSIONS.get(selected_role, [])
        if selected_query not in allowed_queries:
            messagebox.showerror(
                "Access Denied",
                f"The role '{selected_role}' is not allowed to run this query."
            )
            self.status_var.set("Access denied.")
            return

        query_info = self.QUERY_DEFINITIONS.get(selected_query)
        if not query_info:
            messagebox.showwarning("No Query", "Please select a valid query.")
            return

        try:
            filters = {k: v.get() for k, v in self.filter_vars.items()}
            params = query_info["params"](filters)

            self.cursor.execute(query_info["sql"], params)
            rows = self.cursor.fetchall()

            self.current_rows = rows
            self.display_results(rows)
            self.result_count_var.set(f"Rows: {len(rows)}")
            self.status_var.set(
                f"Role: {selected_role} | Query executed successfully. Rows returned: {len(rows)}"
            )

        except Error as e:
            self.status_var.set("Query execution failed.")
            messagebox.showerror("Query Error", f"An error occurred while running the query.\n\n{e}")

    def display_results(self, rows):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.result_tree["columns"] = ()
        self.sort_states = {}

        if not rows:
            self.result_tree["columns"] = ("message",)
            self.result_tree.heading("message", text="Message")
            self.result_tree.column("message", width=500, anchor="w")
            self.result_tree.insert("", "end", values=("No records found.",), tags=("evenrow",))
            return

        columns = list(rows[0].keys())
        self.result_tree["columns"] = columns

        for col in columns:
            self.result_tree.heading(
                col,
                text=col.replace("_", " ").title(),
                command=lambda c=col: self.sort_treeview_column(c)
            )
            self.result_tree.column(col, width=180, anchor="w")

        for index, row in enumerate(rows):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.result_tree.insert("", "end", values=[row[col] for col in columns], tags=(tag,))

    def sort_treeview_column(self, col):
        if not self.current_rows:
            return

        reverse = self.sort_states.get(col, False)

        def sort_key(item):
            value = item.get(col)
            if value is None:
                return ""
            return str(value).lower()

        self.current_rows.sort(key=sort_key, reverse=reverse)
        self.sort_states[col] = not reverse
        self.display_results(self.current_rows)

    def export_results_to_csv(self):
        if not self.current_rows:
            messagebox.showwarning("No Data", "There are no query results to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Query Results"
        )

        if not file_path:
            return

        try:
            columns = list(self.current_rows[0].keys())
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerows(self.current_rows)

            self.status_var.set(f"Results exported successfully to {file_path}")
            messagebox.showinfo("Export Complete", "Query results exported successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results.\n\n{e}")

    def clear_results(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.result_tree["columns"] = ()
        self.current_rows = []
        self.result_count_var.set("Rows: 0")
        self.status_var.set("Results cleared.")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()


def main():
    root = tk.Tk()

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(base_dir, "Univeristy_Icon.png"),
            os.path.join(base_dir, "University_Icon.png"),
            os.path.join(base_dir, "assets", "Univeristy_Icon.png"),
            os.path.join(base_dir, "assets", "University_Icon.png"),
        ]

        for icon_path in possible_paths:
            if os.path.exists(icon_path):
                app_icon = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, app_icon)
                root._app_icon_ref = app_icon
                break
    except Exception as e:
        print("Icon load error:", e)

    app = UniversityDBApp(root)

    def on_closing():
        app.close_connection()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    print("Launching app...")
    main()