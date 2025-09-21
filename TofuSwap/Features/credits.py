# Credits
import tkinter as tk
from tkinter import ttk
import webbrowser

def make_link(parent, text, url):
    link = tk.Label(parent, text=text, 
                     font=("Segoe UI", 15, "underline"), 
                     bg="#f7f2e7");
    link.pack(pady=10)
    link.bind("<Button-1>", lambda e: webbrowser.open_new(url))
    return link

def create_credits_panel(parent, switch_callback):
    """
    Creates the Credits panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#f7f2e7")
    
    title = tk.Label(frame, text="Credits", 
                     font=("Segoe UI", 40), 
                     bg="#f7f2e7")
    title.pack(pady=10);

    tk.Label(frame, text="CHENG Po Hei", 
                     font=("Segoe UI", 20), 
                     bg="#f7f2e7").pack(pady=10);
    make_link(frame, "github.com/iceheart-ac", "github.com/iceheart-ac");
    
    tk.Label(frame, text="CHOI Kui Wang, Joshua", 
                     font=("Segoe UI", 20), 
                     bg="#f7f2e7").pack(pady=10);
    make_link(frame, "github.com/joshuaSYSS", "github.com/joshuaSYSS");

    back_btn = ttk.Button(frame, text="返回選單",
                          command=lambda: switch_callback("menu"))
    back_btn.pack(pady=10)

    return frame