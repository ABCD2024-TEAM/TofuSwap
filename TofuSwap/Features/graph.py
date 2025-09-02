# Graph and visualization for ingredients
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Features.testnetwork import visualize_network

def create_graph_panel(parent, switch_callback):
    """
    Creates the Graph/Visualization panel UI.
    :param parent: parent widget (usually container frame)
    :param switch_callback: function to call with target scene name
    """
    frame = tk.Frame(parent, bg="#f7f2e7")

    title = tk.Label(frame, text="Graph Visualization",
             font=("Segoe UI", 40, "bold"),
             bg="#f7f2e7")
    title.pack(pady=10)

    # Add the network graph
    fig = visualize_network()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

    back_btn = ttk.Button(frame, text="Back to Menu",
                          command=lambda: switch_callback("menu"))
    back_btn.pack(pady=10)

    return frame
