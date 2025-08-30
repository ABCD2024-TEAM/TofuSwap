import tkinter as tk
from tkinter import ttk
from Features import importDataset
import os

df = importDataset.getDataset()
base_dir = os.path.dirname(os.path.abspath(__file__))

def create_viewSaved_panel(parent, switch_callback):
    """
    Creates the Viewing Saved Dishes panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#f7f2e7")

    title = tk.Label(frame, text="View Saved Dishes",
             font=("Segoe UI", 40, "bold"),
             bg="#f7f2e7")
    title.pack(pady=10)
    
    

    back_btn = ttk.Button(frame, text="Back to Save Dishes Menu",
                          command=lambda: switch_callback("save"))
    back_btn.pack(pady=10)

    return frame
