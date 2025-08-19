# Find similar food
import tkinter as tk
from tkinter import ttk

def create_similar_panel(parent, switch_callback):
    """
    Creates the Similar panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#ffffff")

    tk.Label(frame, text="Similar",
             font=("Segoe UI", 16, "bold"),
             bg="#ffffff").pack(pady=10)

    back_btn = ttk.Button(frame, text="Back to Menu",
                          command=lambda: switch_callback("menu"))
    back_btn.pack(pady=10)

    return frame
