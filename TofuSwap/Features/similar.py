# Find similar food
import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox
from tkinter import Listbox, Entry, END, Label
from Features import importDataset

frame = None;
df = importDataset.getDataset();
first_column = df.iloc[:, 0].astype(str).tolist()

def create_similar_panel(parent, switch_callback):
    """
    Creates the Similar panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    global frame
    global entry, listbox, detail_label
    frame = tk.Frame(parent, bg="#f7f2e7")

    title = tk.Label(frame, text="Similar",
             font=("Segoe UI", 40, "bold"),
             bg="#f7f2e7")
    title.pack(pady=10)
    
    frame.input_var = tk.StringVar()
    input_frame = tk.Frame(frame, bg="#f7f2e7")
    input_frame.pack(pady=10)

    entry = Entry(frame, width=100)
    entry.pack()
    entry.bind('<KeyRelease>', search)
    
    listbox = Listbox(frame, width=100)
    listbox.pack()
    listbox.bind('<<ListboxSelect>>', show_details)
    
    detail_label = Label(frame, text="", wraplength=300)
    detail_label.pack()
    
    for item in first_column:
        listbox.insert(END, item)
        
    find_similar_btn = ttk.Button(frame, text="Find Similar", command=lambda: show_similar())
    find_similar_btn.pack(pady=10)

    back_btn = ttk.Button(frame, text="Back to Menu",
                          command=lambda: switch_callback("menu"))
    back_btn.pack(pady=10)

    return frame

def show_similar():
    
    return;

def search(event):
    query = entry.get().lower()
    listbox.delete(0, END)
    for item in first_column:
        if query in item.lower():
            listbox.insert(END, item)
    detail_label.config(text="")  # Clear details on new search

def show_details(event):
    selection = listbox.curselection()
    if selection:
        selected_value = listbox.get(selection[0])
        row = df[df.iloc[:, 0].astype(str) == selected_value]
        if not row.empty:
            # Get columns 2-7, skipping NaN
            cols_2_7 = [str(val) for val in row.iloc[0, 1:7] if pd.notna(val)]
            line1 = ", ".join(cols_2_7)
            # Get column 8, skipping NaN
            col8 = str(row.iloc[0, 7]) if pd.notna(row.iloc[0, 7]) else ""
            # Get column 9, skipping NaN
            col9 = str(row.iloc[0, 8]) if pd.notna(row.iloc[0, 8]) else ""
            # Build details string
            details = "材料: "
            details += line1
            if col8:
                details += f"\n烹調方式: {col8}"
            if col9:
                details += f"\n顔色: {col9}"
            detail_label.config(text=f"{details}")