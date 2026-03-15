import tkinter as tk
from tkinter import ttk


def get_color_scheme():
    """Return the color palette for the app."""
    return {
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


def configure_styles(style, colors):
    """Configure ttk styles for the app."""
    style.theme_use("clam")

    style.configure("Card.TFrame", background=colors["bg_card"])
    style.configure(
        "Title.TLabel",
        font=("Segoe UI", 22, "bold"),
        background=colors["bg_header"],
        foreground=colors["text_light"],
        padding=(6, 4)
    )
    # Add the rest of your style configurations here


def create_accessible_button(parent, text, icon, colors, command):
    """Reusable function to create styled buttons."""
    btn = tk.Button(
        parent,
        text=text,
        image=icon,
        compound="left",
        command=command,
        bg=colors["button_run"],
        activebackground=colors["button_run_hover"],
        fg=colors["button_text"],
        activeforeground=colors["button_text"],
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=8,
        bd=0,
        relief="flat",
        cursor="hand2"
    )
    btn.default_bg = colors["button_run"]
    btn.hover_bg = colors["button_run_hover"]
    btn.bind("<Enter>", lambda event, b=btn: on_button_hover_in(b))
    btn.bind("<Leave>", lambda event, b=btn: on_button_hover_out(b))
    return btn


def on_button_hover_in(button):
    """Handle mouse enter event for buttons."""
    button.configure(bg=button.hover_bg)


def on_button_hover_out(button):
    """Handle mouse leave event for buttons."""
    button.configure(bg=button.default_bg)


def create_hoverable_control_wrapper(parent, colors):
    """Create a hoverable wrapper for input controls."""
    wrapper = tk.Frame(
        parent,
        bg=colors["border"],
        highlightthickness=2,
        highlightbackground=colors["border"],
        highlightcolor=colors["hover_outline"],
        bd=0
    )
    return wrapper


def bind_control_hover(wrapper, widget, colors):
    """Bind hover/focus events to control wrappers."""
    def hover_in(event=None):
        wrapper.config(
            highlightbackground=colors["hover_outline"],
            bg=colors["hover_outline"]
        )

    def hover_out(event=None):
        wrapper.config(
            highlightbackground=colors["border"],
            bg=colors["border"]
        )

    wrapper.bind("<Enter>", hover_in)
    wrapper.bind("<Leave>", hover_out)
    widget.bind("<Enter>", hover_in)
    widget.bind("<Leave>", hover_out)
    widget.bind("<FocusIn>", hover_in)
    widget.bind("<FocusOut>", hover_out)