from tkinter import messagebox


def validate_role_permissions(app):
    """Check if the selected role has permission to run the selected query."""
    selected_role = app.role_var.get()
    selected_query = app.query_var.get()
    allowed_queries = app.ROLE_PERMISSIONS.get(selected_role, [])

    if selected_query not in allowed_queries:
        messagebox.showerror(
            "Access Denied",
            f"The role '{selected_role}' is not allowed to run this query.\n\n"
            f"Allowed queries for {selected_role}: {', '.join(allowed_queries[:3])}..."
        )
        app.status_var.set("Access denied.")
        return False

    return True


def update_role_ui(app):
    """Update UI when the selected role changes (update query dropdown/info)."""
    selected_role = app.role_var.get()
    allowed_queries = app.ROLE_PERMISSIONS.get(selected_role, [])

    app.role_info_label.config(text=selected_role)
    app.query_combo["values"] = allowed_queries

    if allowed_queries:
        app.query_var.set(allowed_queries[0])
        app.on_query_change()
        app.status_var.set(f"Role changed to {selected_role}. Available queries updated.")
    else:
        app.query_var.set("")
        app.query_description.config(state="normal")
        app.query_description.delete("1.0", "end")
        app.query_description.config(state="disabled")
        app.status_var.set(f"No queries available for role: {selected_role}")