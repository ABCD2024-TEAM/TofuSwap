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

    # Title
    title = tk.Label(frame, text="All Dishes",
                     font=("Segoe UI", 30, "bold"),
                     bg="#f7f2e7")
    title.pack(pady=10)

    # Treeview setup
    columns = ("Name",)
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tree.heading("Name", text="Dish Name")
    # force the “Name” column to max out at 200px and not expand
    tree.column("Name", width=200, stretch=False)

    tree.tag_configure("saved", foreground="#888888")    # gray out saved items

    # Scrollbar (optional)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(padx=10)

    # --- REFRESH FUNCTION ---
    def refresh():
        global saved_dishes

        # 1) reload saved_dishes from file
        if os.path.exists(list_file_path):
            with open(list_file_path, "r", encoding="utf-8") as f:
                saved_dishes = [line.strip() for line in f if line.strip()]
        else:
            saved_dishes = []

        # 2) clear existing tree items
        for item in tree.get_children():
            tree.delete(item)

        # 3) re‐populate from dataframe, tagging saved ones
        for i in range(len(df)):
            dish_name = df.iloc[i, 0]
            tag = "saved" if dish_name in saved_dishes else ""
            tree.insert("", tk.END, values=(dish_name,), tags=(tag,))

    # initial population
    refresh()

    # --- SAVE BUTTON LOGIC ---
    def save_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("無選擇", "請選擇要保存的菜餚")
            return

        newly_saved = 0
        for sel in selected:
            dish_name = tree.item(sel, "values")[0]
            if dish_name not in saved_dishes:
                # append to file
                with open(list_file_path, "a", encoding="utf-8") as f:
                    f.write(dish_name + "\n")
                newly_saved += 1

        if newly_saved:
            messagebox.showinfo("Saved", f"儲存了 {newly_saved} 道新菜餚")
            refresh()   # update the list immediately
        else:
            messagebox.showinfo("沒有變化", "Selected dish(es) already saved.")

    ttk.Button(frame, text="保存所選菜餚", command=save_selected).pack(pady=5)

    # Navigation buttons
    btn_frame = tk.Frame(frame, bg="#f7f2e7")
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="查看已保存的菜餚",
               command=lambda: switch_callback("viewSaved"))\
       .grid(row=0, column=0, padx=5)

    ttk.Button(btn_frame, text="獲取推薦",
               command=lambda: switch_callback("recommend"))\
       .grid(row=0, column=1, padx=5)

    # Back button
    ttk.Button(frame, text="返回選單",
               command=lambda: switch_callback("menu")).pack(pady=10)

    # Expose refresh so your main app can call it on every show
    frame.refresh = refresh
    return frame
