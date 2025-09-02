# Find similar food (Hybrid Jaccard + Embedding)
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import Listbox, Entry, END, Label
from Features import importDataset
from sentence_transformers import SentenceTransformer, util

# -------------------------
# Load dataset
# -------------------------
frame = None
df = importDataset.getDataset()
first_column = df.iloc[:, 0].astype(str).tolist()
attributes = df.iloc[:, 1:]

# -------------------------
# Load embedding model & precompute name embeddings
# -------------------------
embed_model = SentenceTransformer('shibing624/text2vec-base-chinese')
name_embeddings = embed_model.encode(first_column, normalize_embeddings=True)

# -------------------------
# Weighted Jaccard Similarity
# -------------------------
def weighted_jaccard_similarity(r1, r2, weights):
    intersection = 0
    union = 0
    for i in range(len(r1)):
        w = weights[i]
        union += w
        hassame = False
        for j in range(len(r2)):
            if r1[i] == r2[j]:
                intersection += w
                hassame = True
                break
        if not hassame:
            union += w
    return intersection / union if union else 0

# -------------------------
# UI Creation
# -------------------------
def create_similar_panel(parent, switch_callback):
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

# -------------------------
# Similarity Search
# -------------------------
def show_similar(event=None):
    selection = listbox.curselection()
    if selection:
        selected_value = listbox.get(selection[0])
        row_index = df.index[df.iloc[:, 0].astype(str) == selected_value].tolist()[0]

        # Weighted Jaccard weights: col2=4, col3-7=2, col8-9=1
        weights = [4] + [2]*5 + [1]*2

        similarities = []
        for i in range(len(df)):
            if i != row_index:
                # Weighted Jaccard on attributes
                jac_sim = weighted_jaccard_similarity(
                    attributes.iloc[row_index].tolist(),
                    attributes.iloc[i].tolist(),
                    weights
                )

                # Embedding similarity on names
                emb_sim = util.cos_sim(
                    name_embeddings[row_index],
                    name_embeddings[i]
                ).item()

                # Hybrid score
                hybrid_score = 0.7 * jac_sim + 0.3 * emb_sim

                similarities.append((df.iloc[i, 0], hybrid_score))

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar = similarities[:5]
        open_new_window(top_similar)
    return

# -------------------------
# Search & Details
# -------------------------
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
            cols_2_7 = [str(val) for val in row.iloc[0, 1:7] if pd.notna(val)]
            line1 = ", ".join(cols_2_7)
            col8 = str(row.iloc[0, 7]) if pd.notna(row.iloc[0, 7]) else ""
            col9 = str(row.iloc[0, 8]) if pd.notna(row.iloc[0, 8]) else ""
            details = "材料: " + line1
            if col8:
                details += f"\n烹調方式: {col8}"
            if col9:
                details += f"\n顔色: {col9}"
            detail_label.config(text=f"{details}")

# -------------------------
# Similar Foods Window
# -------------------------
def open_new_window(top_similar):
    win = tk.Toplevel()
    win.title("Similar Foods")
    win.geometry("800x450")
    win.configure(bg="#f7f2e7")  # window background

    # Main container: Canvas + Scrollbar + Frame inside Canvas
    container = tk.Frame(win, bg="#f7f2e7")
    container.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container, bg="#f7f2e7", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f7f2e7")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
                     justify="left", wraplength=480,
                     bg="#f7f2e7").pack(
                         pady=10, padx=10, fill=tk.X
                     )
            tk.Label(scrollable_frame, text=details,
                     font=("Segoe UI", 15), anchor="w",
                     justify="left", wraplength=480,
                     bg="#f7f2e7").pack(
                         pady=5, padx=20, fill=tk.X
                     )

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

