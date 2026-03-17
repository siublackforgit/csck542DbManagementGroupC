import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from app.db.connection import DatabaseManager
from app.db.queries import get_query_definitions, get_role_permissions
from app.db.filters import populate_all_filter_values, on_department_change, on_lecturer_change
from app.utils.permissions import validate_role_permissions, update_role_ui
from app.utils.csv_export import export_results_to_csv
from app.utils.sorting import sort_treeview_column
from app.ui.styles import (
    get_color_scheme,
    configure_styles,
    create_accessible_button,
    create_hoverable_control_wrapper,
    bind_control_hover,
    on_button_hover_in,
    on_button_hover_out
)
from .icons import load_app_icons

class UniversityDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Database Management and Query System")
        self.root.geometry("1550x930")
        self.root.minsize(1320, 800)

        # Initialize core dependencies
        self.db_manager = DatabaseManager()
        self.colors = get_color_scheme()
        self.style = ttk.Style()
        self.QUERY_DEFINITIONS = get_query_definitions()
        self.ROLE_PERMISSIONS = get_role_permissions()

        # UI State Variables
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

        # UI References
        self.filter_combo_widgets = {}
        self.filter_frames = {}
        self.current_rows = []
        self.sort_states = {}
        self.role_info_label = None
        self.query_combo = None
        self.query_description = None
        self.result_tree = None

        # Load icons and configure styles
        self.icons = load_app_icons()
        configure_styles(self.style, self.colors)

        # Build UI and initialize
        self.build_layout()
        self._connect_db()
        self.populate_all_filter_values = populate_all_filter_values  # Bind DB filter logic
        self.populate_all_filter_values(self)
        self.on_role_change()

    def _connect_db(self):
        """Wrapper for DB connection with UI feedback"""
        success, msg = self.db_manager.connect()
        self.status_var.set(msg)
        if not success:
            messagebox.showerror("Database Connection Error", msg)

    def build_layout(self):
        """Build the full UI layout (your original build_layout logic)"""
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Header Section
        header_bg = tk.Frame(self.root, bg=self.colors["bg_header"], height=78)
        header_bg.grid(row=0, column=0, sticky="ew")
        header_bg.grid_propagate(False)

        header_inner = tk.Frame(header_bg, bg=self.colors["bg_header"])
        header_inner.pack(expand=True, fill="both")

        title_container = tk.Frame(header_inner, bg=self.colors["bg_header"])
        title_container.pack(pady=(6, 0))

        if self.icons["header"]:
            icon_label = tk.Label(
                title_container,
                image=self.icons["header"],
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

        # Dashboard Frame (Role/Query/Project Info)
        dashboard_frame = ttk.Frame(self.root, style="Card.TFrame")
        dashboard_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(10, 8))
        for i in range(3):
            dashboard_frame.grid_columnconfigure(i, weight=1, uniform="dash")

        self.build_role_filters_dashboard(dashboard_frame)
        self.build_query_dashboard(dashboard_frame)
        self.build_project_info_dashboard(dashboard_frame)

        # Action Buttons Frame
        action_frame = ttk.Frame(self.root, style="Card.TFrame")
        action_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 8))
        
        BTN_WIDTH = 140    
        BTN_HEIGHT = 38

        # Run Query Button
        self.run_button = create_accessible_button(
            parent=action_frame,
            text="Run Query",
            icon=self.icons.get("run"),
            colors=self.colors,
            command=self.run_selected_query
        )
        self.run_button.configure(
            bg=self.colors["button_run"],
            activebackground=self.colors["button_run_hover"],
            width=BTN_WIDTH,
            height=BTN_HEIGHT
        )
        self.run_button.default_bg = self.colors["button_run"]
        self.run_button.hover_bg   = self.colors["button_run_hover"]
        self.run_button.pack(side="left", padx=(0, 10))

        # Clear Results Button
        self.clear_button = create_accessible_button(
            parent=action_frame,
            text="Clear Results",
            icon=self.icons.get("clear"),
            colors=self.colors,
            command=self.clear_results
        )
        self.clear_button.configure(
            bg=self.colors["button_clear"],
            activebackground=self.colors["button_clear_hover"],
            width=BTN_WIDTH,
            height=BTN_HEIGHT
        )
        self.clear_button.default_bg = self.colors["button_clear"]
        self.clear_button.hover_bg   = self.colors["button_clear_hover"]
        self.clear_button.pack(side="left", padx=(0, 10))

        # Refresh Filters Button
        self.refresh_button = create_accessible_button(
            parent=action_frame,
            text="Refresh Filters",
            icon=self.icons.get("refresh"),
            colors=self.colors,
            command=self.refresh_filters
        )
        self.refresh_button.configure(
            bg=self.colors["button_refresh"],
            activebackground=self.colors["button_refresh_hover"],
            width=BTN_WIDTH,
            height=BTN_HEIGHT
        )
        self.refresh_button.default_bg = self.colors["button_refresh"]
        self.refresh_button.hover_bg   = self.colors["button_refresh_hover"]
        self.refresh_button.pack(side="left", padx=(0, 10))

        # Export CSV Button
        self.export_button = create_accessible_button(
            parent=action_frame,
            text="Export CSV",
            icon=self.icons.get("csv"),   
            colors=self.colors,
            command=lambda: export_results_to_csv(self.current_rows, self.status_var)
        )
        self.export_button.configure(
            bg=self.colors["button_export"],
            activebackground=self.colors["button_export_hover"],
            width=BTN_WIDTH,
            height=BTN_HEIGHT
        )
        self.export_button.default_bg = self.colors["button_export"]
        self.export_button.hover_bg   = self.colors["button_export_hover"]
        self.export_button.pack(side="left", padx=(0, 10))

        # Result Count Label
        ttk.Label(
            action_frame,
            textvariable=self.result_count_var,
            style="PanelValue.TLabel"
        ).pack(side="right", padx=(10, 0))

        # Results Section
        self.build_results_section()

        # Status Bar
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

    def build_role_filters_dashboard(self, parent):
        """Build role/filter UI (your original logic)"""
        frame = ttk.LabelFrame(
            parent,
            text="1. Role Access and Dynamic Filters",
            style="Section.TLabelframe"
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        frame.grid_columnconfigure(0, weight=1)

        current_row = 0

        # Role Selection
        ttk.Label(frame, text="Select Role:").grid(
            row=current_row, column=0, sticky="w", padx=10, pady=(8, 2)
        )
        current_row += 1

        role_wrapper = create_hoverable_control_wrapper(frame, self.colors)
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
        bind_control_hover(role_wrapper, self.role_combo, self.colors)
        current_row += 1

        # Current Access Level
        ttk.Label(frame, text="Current Access Level:").grid(
            row=current_row, column=0, sticky="w", padx=10, pady=(0, 2)
        )
        current_row += 1

        self.role_info_label = ttk.Label(frame, text="Student", style="PanelValue.TLabel")
        self.role_info_label.grid(
            row=current_row, column=0, sticky="w", padx=10, pady=(0, 8)
        )
        current_row += 1

        # Filter Dropdowns
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

            combo_wrapper = create_hoverable_control_wrapper(container, self.colors)
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
            bind_control_hover(combo_wrapper, combo, self.colors)

            current_row += 1

        # Bind filter change events
        self.filter_combo_widgets["department"].bind(
            "<<ComboboxSelected>>",
            lambda event: on_department_change(self)
        )
        self.filter_combo_widgets["lecturer"].bind(
            "<<ComboboxSelected>>",
            lambda event: on_lecturer_change(self)
        )

    def build_query_dashboard(self, parent):
        """Build query selection UI (your original logic)"""
        frame = ttk.LabelFrame(parent, text="2. Query Selection and Description", style="Section.TLabelframe")
        frame.grid(row=0, column=1, sticky="nsew", padx=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        ttk.Label(frame, text="Choose Query:").grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))

        query_wrapper = create_hoverable_control_wrapper(frame, self.colors)
        query_wrapper.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))

        self.query_combo = ttk.Combobox(
            query_wrapper,
            textvariable=self.query_var,
            state="readonly",
            style="Accessible.TCombobox"
        )
        self.query_combo.pack(fill="x")
        self.query_combo.bind("<<ComboboxSelected>>", lambda event: self.on_query_change())
        bind_control_hover(query_wrapper, self.query_combo, self.colors)

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
        """Build project info UI (your original logic)"""
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

    def build_results_section(self):
        """Build results treeview UI (your original logic)"""
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

    def on_role_change(self):
        """Update UI when role changes (delegates to utils/permissions.py)"""
        update_role_ui(self)

    def on_query_change(self):
        """Update query description and active filters"""
        selected_query = self.query_var.get()
        query_info = self.QUERY_DEFINITIONS.get(selected_query)

        if not query_info:
            return

        # Update description
        self.query_description.config(state="normal")
        self.query_description.delete("1.0", tk.END)
        self.query_description.insert(tk.END, query_info["description"])
        self.query_description.config(state="disabled")

        # Show/hide filters
        active_filters = query_info["filters"]
        for key, frame in self.filter_frames.items():
            if key in active_filters:
                frame.grid()
            else:
                frame.grid_remove()

        self.status_var.set(f"Selected query: {selected_query}")

    def refresh_filters(self):
        """Refresh filter values from DB"""
        self.populate_all_filter_values(self)
        self.on_query_change()
        self.status_var.set("Filters refreshed from database.")

    def run_selected_query(self):
        """Execute selected query (with role permission check)"""
        if not self.db_manager.cursor:
            messagebox.showwarning("No Connection", "No active database connection.")
            return

        # Validate role permissions
        if not validate_role_permissions(self):
            return

        selected_query = self.query_var.get()
        query_info = self.QUERY_DEFINITIONS.get(selected_query)
        if not query_info:
            messagebox.showwarning("No Query", "Please select a valid query.")
            return

        # Execute query
        try:
            filters = {k: v.get() for k, v in self.filter_vars.items()}
            params = query_info["params"](filters)
            rows, msg = self.db_manager.run_query(query_info["sql"], params)

            if rows is None:
                self.status_var.set("Query execution failed.")
                messagebox.showerror("Query Error", msg)
                return

            # Display results
            self.current_rows = rows
            self.display_results(rows)
            self.result_count_var.set(f"Rows: {len(rows)}")
            self.status_var.set(
                f"Role: {self.role_var.get()} | Query executed successfully. Rows returned: {len(rows)}"
            )

        except Exception as e:
            self.status_var.set("Query execution failed.")
            messagebox.showerror("Query Error", f"An error occurred while running the query.\n\n{e}")

    def display_results(self, rows):
        """Display query results in treeview"""
        # Clear existing results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree["columns"] = ()
        self.sort_states = {}

        if not rows:
            # Show "No records" message
            self.result_tree["columns"] = ("message",)
            self.result_tree.heading("message", text="Message")
            self.result_tree.column("message", width=500, anchor="w")
            self.result_tree.insert("", "end", values=("No records found.",), tags=("evenrow",))
            return

        # Populate results
        columns = list(rows[0].keys())
        self.result_tree["columns"] = columns

        for col in columns:
            self.result_tree.heading(
                col,
                text=col.replace("_", " ").title(),
                command=lambda c=col: sort_treeview_column(self, c)
            )
            self.result_tree.column(col, width=180, anchor="w")

        for index, row in enumerate(rows):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.result_tree.insert("", "end", values=[row[col] for col in columns], tags=(tag,))

    def clear_results(self):
        """Clear results from treeview"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree["columns"] = ()
        self.current_rows = []
        self.result_count_var.set("Rows: 0")
        self.status_var.set("Results cleared.")

    def close(self):
        """Clean up resources"""
        self.db_manager.close()