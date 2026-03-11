import csv
import os
from tkinter import filedialog, messagebox

def export_results_to_csv(current_rows, status_var):
    """
    Export query results to a CSV file
    """
    if not current_rows:
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
        columns = list(current_rows[0].keys())
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(current_rows)

        status_var.set(f"Results exported successfully to {os.path.basename(file_path)}")
        messagebox.showinfo("Export Complete", "Query results exported successfully!")

    except Exception as e:
        status_var.set("Export failed.")
        messagebox.showerror("Export Error", f"Failed to export results:\n\n{e}")