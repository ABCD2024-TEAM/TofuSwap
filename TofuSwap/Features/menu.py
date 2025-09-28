import tkinter as tk
from tkinter import ttk
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
graph_file_path = os.path.join(base_dir, "../Images", "graph.png")
search_file_path = os.path.join(base_dir, "../Images", "search.png")
save_file_path = os.path.join(base_dir, "../Images", "save.png")
info_file_path = os.path.join(base_dir, "../Images", "info.png")

def create_menu_panel(parent, switch_callback):
    # Colors
    BG_COLOR = "#f7f2e7"
    ACCENT_COLOR = "#2e7d32"
    BTN_BG = "#4caf50"
    BTN_FG = "white"
    BTN_HOVER = "#45a049"

    frame = tk.Frame(parent, bg=BG_COLOR)

    # ttk style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Modern.TButton",
        font=("Segoe UI", 14, "bold"),
        padding=(14, 8),   # add left padding so content isn't glued to the edge
        background=BTN_BG,
        foreground=BTN_FG,
        borderwidth=0
    )
    style.map(
        "Modern.TButton",
        background=[("active", BTN_HOVER)],
        foreground=[("active", "white")]
    )
    # Critical: left-align the internal label element
    style.layout(
        "Modern.TButton",
        [
            ("Button.padding", {
                "sticky": "nswe",
                "children": [
                    ("Button.label", {"sticky": "w"})   # pin to left
                ]
            })
        ]
    )

    # Title with closer shadow
    shadow = tk.Label(frame, text="TofuSwap",
                      font=("Segoe UI", 40, "bold"),
                      fg="gray80", bg=BG_COLOR)
    shadow.place(x=3, y=33)

    title_label = tk.Label(frame, text="TofuSwap",
                           font=("Segoe UI", 40, "bold"),
                           fg=ACCENT_COLOR, bg=BG_COLOR)
    title_label.pack(pady=(40, 20))

    # Load icons (subsample to taste; try 2–4 for typical sizes)
    icons = {
        #"graph": tk.PhotoImage(file=graph_file_path).subsample(16, 16),
        "similar": tk.PhotoImage(file=search_file_path).subsample(16, 16),
        "save": tk.PhotoImage(file=save_file_path).subsample(16, 16),
        "credits": tk.PhotoImage(file=info_file_path).subsample(16, 16),
    }

    # Buttons with icons
    buttons = [
        #("建立食品成分圖表", "graph"),
        ("尋找類似的食物", "similar"),
        ("保存食物", "save"),
        ("製作人員", "credits")
    ]

    for text, target in buttons:
        btn = ttk.Button(
            frame,
            text=text,
            style="Modern.TButton",
            image=icons[target],
            compound="left",              # icon on the left of text
            command=lambda t=target: switch_callback(t),
            width=28                      # consistent width; content now left-aligned
        )
        btn.pack(pady=6)                  # keep buttons centered; content is left-aligned inside

    # Prevent images from being GC'd
    frame.icons = icons

    return frame
