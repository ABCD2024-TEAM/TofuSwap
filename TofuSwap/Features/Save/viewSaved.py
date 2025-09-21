import tkinter as tk
from tkinter import ttk
from Features import importDataset
import os

df = importDataset.getDataset()
base_dir = os.path.dirname(os.path.abspath(__file__))
list_file_path = os.path.join(base_dir, "savedDishes", "list.txt")
saved_dishes = []

def create_viewSaved_panel(parent, switch_callback):
    frame = tk.Frame(parent, bg="#f7f2e7")

    title = tk.Label(frame, text="View Saved Dishes",
                     font=("Segoe UI", 40, "bold"),
                     bg="#f7f2e7")
    title.pack(pady=10)

    # This inner frame will hold all the dish‐rows
    content = tk.Frame(frame, bg="#f7f2e7")
    content.pack(fill="both", expand=True)

    def refresh():
        # 1) clear out old widgets
        for w in content.winfo_children():
            w.destroy()

        # 2) re-read the file
        with open(list_file_path, "r", encoding="utf-8") as f:
            saved = [line.strip() for line in f if line.strip()]

        if not saved:
            tk.Label(content,
                     text="未找到已保存的菜餚。\n請保存一些菜餚以獲取推薦。",
                     font=("Segoe UI", 14),
                     fg="#555555",
                     bg="#f7f2e7",
                     justify="center")\
              .pack(pady=30)
        else:
            for dish_name in saved:
                match = df[df.iloc[:,0].str.strip() == dish_name.strip()]
                if match.empty:
                    continue
                row = match.iloc[0]

                dish_frame = tk.Frame(content, bg="#f7f2e7")
                dish_frame.pack(fill="x", padx=20, pady=5)

                info = tk.Frame(dish_frame, bg="#f7f2e7")
                info.pack(side="left", fill="x", expand=True)

                tk.Label(info,
                         text=row.iloc[0],
                         font=("Segoe UI", 16, "bold"),
                         anchor="w",
                         bg="#f7f2e7")\
                  .pack(fill="x")

                ingr = ", ".join(str(x).strip() for x in row.iloc[1:7])
                tk.Label(info,
                         text=f"原料: {ingr}",
                         font=("Segoe UI", 12),
                         anchor="w",
                         bg="#f7f2e7")\
                  .pack(fill="x")

                tk.Label(info,
                         text=f"烹調方法: {row.iloc[7].strip()}",
                         font=("Segoe UI", 12),
                         anchor="w",
                         bg="#f7f2e7")\
                  .pack(fill="x")

                tk.Label(info,
                         text=f"外貌: {row.iloc[8].strip()}",
                         font=("Segoe UI", 12),
                         anchor="w",
                         bg="#f7f2e7")\
                  .pack(fill="x")

                def make_rm(d):
                    def _rm():
                        # remove & rewrite file
                        saved.remove(d)
                        with open(list_file_path, "w", encoding="utf-8") as wf:
                            for sd in saved:
                                wf.write(sd+"\n")
                        # then immediately refresh
                        refresh()
                    return _rm

                ttk.Button(dish_frame,
                           text="消除",
                           command=make_rm(dish_name))\
                   .pack(side="right", padx=10)

    # call it once now
    refresh()

    back_btn = ttk.Button(frame, text="返回保存菜餚菜單",
                          command=lambda: switch_callback("save"))
    back_btn.pack(pady=10)

    # expose refresh so your switch logic can also call frame.refresh()
    frame.refresh = refresh
    return frame
