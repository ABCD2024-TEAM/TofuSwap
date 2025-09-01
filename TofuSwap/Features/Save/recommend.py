import tkinter as tk
from tkinter import ttk
import os
from Features import importDataset
import pandas as pd

saved_dishes = []
df = importDataset.getDataset();
base_dir = os.path.dirname(os.path.abspath(__file__))
list_file_path = os.path.join(base_dir, "savedDishes", "list.txt")

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
    
    # Add code below
    content_frame = tk.Frame(frame, bg="#f7f2e7")
    content_frame.pack(pady=10)

    def refresh():
        # Clear old content
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Read saved dishes
        if os.path.exists(list_file_path):
            with open(list_file_path, "r", encoding="utf-8") as f:
                saved_dishes = [line.strip() for line in f if line.strip()]
        else:
            saved_dishes = []

        if not saved_dishes:
            tk.Label(content_frame,
                    text="No saved dishes found.\nPlease save some dishes to get recommendations.",
                    font=("Segoe UI", 14),
                    bg="#f7f2e7",
                    fg="red").pack(pady=20)
            return

        saved_rows = df[df.iloc[:, 0].isin(saved_dishes)]

        best_score = -1
        best_row = None

        for idx, row in df.iterrows():
            if row.iloc[0] in saved_dishes:
                continue
            score = 0
            for _, srow in saved_rows.iterrows():
                # First ingredient weight 4
                if pd.notna(row.iloc[1]) and pd.notna(srow.iloc[1]) and \
                str(row.iloc[1]).strip().lower() == str(srow.iloc[1]).strip().lower():
                    score += 4

                # Next 5 ingredients weight 2 each
                for i in range(2, 7):
                    if pd.notna(row.iloc[i]) and pd.notna(srow.iloc[i]) and \
                    str(row.iloc[i]).strip().lower() == str(srow.iloc[i]).strip().lower():
                        score += 2

                # Cooking method weight 1
                if pd.notna(row.iloc[7]) and pd.notna(srow.iloc[7]) and \
                str(row.iloc[7]).strip().lower() == str(srow.iloc[7]).strip().lower():
                    score += 1

                # Appearance weight 1
                if pd.notna(row.iloc[8]) and pd.notna(srow.iloc[8]) and \
                str(row.iloc[8]).strip().lower() == str(srow.iloc[8]).strip().lower():
                    score += 1

            if score > best_score:
                best_score = score
                best_row = row

        if best_row is not None:
            name = best_row.iloc[0]
            ingredients = [str(x) for x in best_row.iloc[1:7] if pd.notna(x)]
            method = best_row.iloc[7]
            appearance = best_row.iloc[8]

            tk.Label(content_frame, text=f"Recommended Dish: {name}",
                    font=("Segoe UI", 20, "bold"),
                    bg="#f7f2e7").pack(pady=10)

            tk.Label(content_frame, text="Ingredients:",
                    font=("Segoe UI", 14, "underline"),
                    bg="#f7f2e7").pack()
            tk.Label(content_frame, text=", ".join(ingredients),
                    font=("Segoe UI", 12),
                    bg="#f7f2e7", wraplength=600, justify="left").pack(pady=5)

            tk.Label(content_frame, text="Cooking Method:",
                    font=("Segoe UI", 14, "underline"),
                    bg="#f7f2e7").pack()
            tk.Label(content_frame, text=method,
                    font=("Segoe UI", 12),
                    bg="#f7f2e7", wraplength=600, justify="left").pack(pady=5)

            tk.Label(content_frame, text="Appearance:",
                    font=("Segoe UI", 14, "underline"),
                    bg="#f7f2e7").pack()
            tk.Label(content_frame, text=appearance,
                    font=("Segoe UI", 12),
                    bg="#f7f2e7", wraplength=600, justify="left").pack(pady=5)
        else:
            tk.Label(content_frame,
                    text="No similar dishes found.",
                    font=("Segoe UI", 14),
                    bg="#f7f2e7",
                    fg="red").pack(pady=20)


    # Call refresh when frame is created
    refresh();
    # Add code above


    back_btn = ttk.Button(frame, text="Back to Save Dishes Menu",
                          command=lambda: switch_callback("save"))
    back_btn.pack(pady=10)

    frame.refresh = refresh;
    return frame
