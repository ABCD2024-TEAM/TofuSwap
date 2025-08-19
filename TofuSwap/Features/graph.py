# Graph and visualization for ingredients
import tkinter as tk
from tkinter import ttk

def create_graph_panel(parent, switch_callback):
    """
    Creates the Graph/Visualization panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#ffffff")

    tk.Label(frame, text="Graph Visualization",
             font=("Segoe UI", 16, "bold"),
             bg="#ffffff").pack(pady=10)

    back_btn = ttk.Button(frame, text="Back to Menu",
                          command=lambda: switch_callback("menu"))
    back_btn.pack(pady=10)

    return frame
