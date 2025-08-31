import tkinter as tk
from tkinter import ttk, messagebox
from Features import importDataset
import os

df = importDataset.getDataset()
saved_dishes = []
base_dir = os.path.dirname(os.path.abspath(__file__))
list_file_path = os.path.join(base_dir, "savedDishes", "list.txt")

def create_save_panel(parent, switch_callback):
    frame = tk.Frame(parent, bg="#f7f2e7")

    title = tk.Label(frame, text="All Dishes",
                     font=("Segoe UI", 30, "bold"),
                     bg="#f7f2e7")
    title.pack(pady=10)
    
    # Build the path to savedDishes/list.txt
    list_file_path = os.path.join(base_dir, "savedDishes", "list.txt")

    # Read all lines into a list, stripping the newline characters
    with open(list_file_path, "r", encoding="utf-8") as f:
        saved_dishes = [line.strip() for line in f if line.strip()]

    # Table 
    columns = ("Name")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tree.heading("Name", text="Dish Name")

    # Populate using iloc
    for i in range(len(df)):
        dish_name = df.iloc[i, 0]   # first column
        tree.insert("", tk.END, values=(dish_name))

    tree.pack(pady=10)
    
    

    # Save button
    def save_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a dish to save.")
            return
        for sel in selected:
            dish_name = tree.item(sel, "values")[0]
            if dish_name not in saved_dishes:
                saved_dishes.append(dish_name)
                
                # Append content instead of overwriting
                with open(list_file_path, "a", encoding="utf-8") as f:
                    f.write(dish_name + "\n");
        messagebox.showinfo("Saved", f"Saved {len(selected)} dish(es).")

    ttk.Button(frame, text="Save Selected Dish", command=save_selected).pack(pady=5)

    # Navigation buttons
    btn_frame = tk.Frame(frame, bg="#f7f2e7")
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="See Saved Dishes",
               command=lambda: switch_callback("viewSaved")).grid(row=0, column=0, padx=5)

    ttk.Button(btn_frame, text="Get Recommendations",
               command=lambda: switch_callback("recommend")).grid(row=0, column=1, padx=5)

    # Back button
    ttk.Button(frame, text="Back to Menu",
               command=lambda: switch_callback("menu")).pack(pady=10)

    return frame
