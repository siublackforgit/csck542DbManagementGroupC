import os
import tkinter as tk
from typing import Optional, Dict, List


# Global reference store to prevent tk.PhotoImage garbage collection
_icon_references = {}


def _get_search_paths() -> List[str]:
    """Build a list of paths to search for icon files."""
    search_paths = []
    try:
        # Get project root (go up 2 levels from app/ui/icons.py)
        ui_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(ui_dir)
        project_root = os.path.dirname(app_dir)

        # Primary path: /assets (top-level assets folder)
        search_paths.append(os.path.join(project_root, "assets"))

        # Fallback paths
        search_paths.append(ui_dir)
        search_paths.append(app_dir)
        search_paths.append(os.getcwd())
    except Exception as e:
        print(f"Warning: Failed to build icon search paths - {e}")
        search_paths = [os.getcwd()]

    return search_paths


def load_single_icon(
    icon_names: List[str],
    subsample: tuple = (1, 1)
) -> Optional[tk.PhotoImage]:
    """Load a single icon from the search paths (handles multiple filename variations)."""
    global _icon_references

    # Get all possible paths to search
    search_paths = _get_search_paths()

    # Check each path for any of the icon names
    for path in search_paths:
        for name in icon_names:
            icon_path = os.path.join(path, name)
            if os.path.exists(icon_path):
                try:
                    # Load and resize the icon
                    icon = tk.PhotoImage(file=icon_path)
                    if subsample != (1, 1):
                        icon = icon.subsample(*subsample)

                    # Store reference to prevent garbage collection
                    _icon_references[icon_path] = icon
                    return icon
                except Exception as e:
                    print(f"Error loading icon {icon_path}: {e}")
                    continue

    # If no icon found
    print(f"Warning: Could not find icon (tried: {', '.join(icon_names)})")
    return None


def load_app_icons() -> Dict[str, Optional[tk.PhotoImage]]:
    """Load all application icons and return them in a structured dictionary."""
    icons = {
        "header": load_single_icon(
            icon_names=["University_Icon.png", "Univeristy_Icon.png"],
            subsample=(6, 6)
        ),
        "run": load_single_icon(
            icon_names=["Run Query.png", "Run_Query.png", "run_query.png"],
            subsample=(14, 14)
        ),
        "clear": load_single_icon(
            icon_names=["Clear Results.png", "Clear_Results.png", "clear_results.png"],
            subsample=(14, 14)
        ),
        "refresh": load_single_icon(
            icon_names=["Refresh.png", "refresh.png"],
            subsample=(14, 14)
        )
    }

    # Log missing icons (for debugging)
    missing_icons = [name for name, icon in icons.items() if icon is None]
    if missing_icons:
        print(f"Warning: Missing icons - {', '.join(missing_icons)}")

    return icons


def clear_icon_references() -> None:
    """Clear global icon references (for clean app shutdown)."""
    global _icon_references
    _icon_references.clear()