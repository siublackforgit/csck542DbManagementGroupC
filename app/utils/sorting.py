def sort_treeview_column(app, col):
    """
    Sort treeview column (asc/desc toggle)
    :param app: Instance of UniversityDBApp (access to current_rows/sort_states/result_tree)
    :param col: Column name to sort by
    """
    if not app.current_rows:
        return

    reverse = app.sort_states.get(col, False)

    def sort_key(item):
        value = item.get(col)
        if value is None:
            return ""

        try:
            return float(value)
        except (ValueError, TypeError):
            return str(value).lower()

    app.current_rows.sort(key=sort_key, reverse=reverse)
    app.sort_states[col] = not reverse   
    app.display_results(app.current_rows)   