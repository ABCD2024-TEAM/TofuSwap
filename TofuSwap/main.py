# Main Code
import tkinter as tk
from tkinter import ttk, messagebox
from Features import credits, graph, importDataset, menu, recommend, save, searchbar, similar, stats

class TofuSwapApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("TofuSwap")
        # self.geometry("500x400")
        self.configure(bg="#f7f2e7")

        # Container to hold all panels
        container = tk.Frame(self, bg="#f7f2e7")
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Pass self.show_frame as switch_callback to scenes
        self.frames["menu"] = menu.create_menu_panel(container, self.show_frame)
        self.frames["graph"] = graph.create_graph_panel(container, self.show_frame)
        self.frames["similar"] = similar.create_similar_panel(container, self.show_frame);
        self.frames["save"] = save.create_save_panel(container, self.show_frame);
        self.frames["credits"] = credits.create_credits_panel(container, self.show_frame);

        # Add new scenes here

        # Stack all frames in same spot
        for frame in self.frames.values():
            frame.place(relwidth=1, relheight=1)

        self.show_frame("menu")

    def show_frame(self, name):
        """Bring a frame to the front"""
        frame = self.frames[name]
        frame.tkraise()



if __name__ == "__main__":
    app = TofuSwapApp()
    app.state("zoomed"); #Start maximized
    app.mainloop()
