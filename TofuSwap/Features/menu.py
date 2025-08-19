# Menu
import tkinter as tk
from tkinter import ttk

def create_menu_panel(parent, switch_callback):
    """
    Creates the Menu panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#f7f2e7")

    title_label = tk.Label(frame, text="TofuSwap",
                           font=("Segoe UI", 40, "bold"),
                           fg="#2e7d32", bg="#f7f2e7")
    title_label.pack(pady=20)

    visualization_button = ttk.Button(
        frame,
        text="Create Visualization of Ingredients",
        command=lambda: switch_callback("graph")
    )
    visualization_button.pack(pady=10)

    similar_button = ttk.Button(
        frame,
        text="Finding Similar Foods",
        command=lambda: switch_callback("similar")
    )
    similar_button.pack(pady=10);

    save_button = ttk.Button(
        frame,
        text="Saved Foods",
        command=lambda: switch_callback("save")
    )
    save_button.pack(pady=10);

    credits_button = ttk.Button(
        frame,
        text="Credits",
        command=lambda: switch_callback("credits")
    )
    credits_button.pack(pady=10);

    # Add new scenes here

    return frame
