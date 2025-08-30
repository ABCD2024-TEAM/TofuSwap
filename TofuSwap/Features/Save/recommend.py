import tkinter as tk
from tkinter import ttk

def create_recommendation_panel(parent, switch_callback):
    """
    Creates the Recommendation panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#f7f2e7")

    title = tk.Label(frame, text="Recommendations",
             font=("Segoe UI", 40, "bold"),
             bg="#f7f2e7")
    title.pack(pady=10)

    back_btn = ttk.Button(frame, text="Back to Save Dishes Menu",
                          command=lambda: switch_callback("save"))
    back_btn.pack(pady=10)

    return frame
