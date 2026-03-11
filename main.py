import tkinter as tk
from app.ui.main_window import UniversityDBApp

def main():
    root = tk.Tk()
    root.title("University Database Management and Query System")
    root.geometry("1550x930")
    root.minsize(1320, 800)

    # Load app icon (optional, move to app/ui/icons.py if needed)
    try:
        import os
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

    # Initialize the app
    app = UniversityDBApp(root)

    # Handle app closure
    def on_closing():
        app.db_manager.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    print("Launching app...")
    main()