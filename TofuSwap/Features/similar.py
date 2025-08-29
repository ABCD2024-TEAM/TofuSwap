# Find similar food
import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox
from tkinter import Listbox, Entry, END, Label
from Features import importDataset
from itertools import combinations

frame = None;
df = importDataset.getDataset();
first_column = df.iloc[:, 0].astype(str).tolist()
attributes = df.iloc[:, 1:]

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


def open_new_window(top_similar):
    win = tk.Toplevel()
    win.title("Similar Foods")
    win.geometry("800x450")

    # Main container: Canvas + Scrollbar + Frame inside Canvas
    container = ttk.Frame(win)
    container.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Make the frame resize properly inside the canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")  # update scrollable area
        )
    )

    # Put the frame in the canvas
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Link scrollbar to canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Layout canvas and scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Populate with your name + details
    for name, sim in top_similar:
        row = df[df.iloc[:, 0].astype(str) == name]
        if not row.empty:
            cols_2_7 = [str(val) for val in row.iloc[0, 1:7] if pd.notna(val)]
            line1 = ", ".join(cols_2_7)
            col8 = str(row.iloc[0, 7]) if pd.notna(row.iloc[0, 7]) else ""
            col9 = str(row.iloc[0, 8]) if pd.notna(row.iloc[0, 8]) else ""
            details = "材料: " + line1
            if col8:
                details += f"\n烹調方式: {col8}"
            if col9:
                details += f"\n顔色: {col9}"

            tk.Label(scrollable_frame, text=name,
                     font=("Segoe UI", 30, "bold"), anchor="w",
                     justify="left", wraplength=480).pack(
                         pady=10, padx=10, fill=tk.X
                     )
            tk.Label(scrollable_frame, text=details,
                     font=("Segoe UI", 15), anchor="w",
                     justify="left", wraplength=480).pack(
                         pady=5, padx=20, fill=tk.X
                     )

    # Optional: Enable mousewheel scrolling on Windows/Mac
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)      # Windows/macOS
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux down

def jaccard_similarity(r1, r2):
    intersection = 0
    union = 0
    
    row1 = r1;
    row2 = r2;

    # Outer loop over attribute positions
    for i in range(len(row1)):
        union += 1;
        hassame = False;
        for j in range(len(row2)):
            a = row1[i]
            b = row2[j]
            if a == b:
                intersection += 1;
                b = None;
                hassame = True;
                break;
        if not hassame:
            union += 1;
    return intersection / union if union else 0

def show_similar(event=None):
    selection = listbox.curselection()
    if selection:
        selected_value = listbox.get(selection[0])
        row_index = df.index[df.iloc[:, 0].astype(str) == selected_value].tolist()[0]
        similarities = []
        for i in range(len(df)):
            if i != row_index:
                sim = jaccard_similarity(attributes.iloc[row_index].tolist(), attributes.iloc[i].tolist())
                similarities.append((df.iloc[i, 0], sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar = similarities[:5]
        open_new_window(top_similar)
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