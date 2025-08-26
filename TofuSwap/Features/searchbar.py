import pandas as pd
import tkinter as tk
from tkinter import Listbox, Entry, END, Label
from Features import importDataset;

# Read CSV
df = importDataset.getDataset();
first_column = df.iloc[:, 0].astype(str).tolist()

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

def run():
    global root
    global entry, listbox, detail_label
    root = tk.Tk()
    root.title("Search CSV First Column")
    
    entry = Entry(root, width=40)
    entry.pack()
    entry.bind('<KeyRelease>', search)
    
    listbox = Listbox(root, width=40)
    listbox.pack()
    listbox.bind('<<ListboxSelect>>', show_details)
    
    detail_label = Label(root, text="", wraplength=300)
    detail_label.pack()
    
    for item in first_column:
        listbox.insert(END, item)
    
    root.mainloop()

