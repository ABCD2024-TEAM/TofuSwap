# Main Code
import tkinter as tk
from tkinter import ttk, messagebox
from Features import *;


class TofuSwapApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("TofuSwap")
        self.geometry("500x400")
        self.configure(bg="#f7f2e7")  # Light beige background


if __name__ == "__main__":
    app = TofuSwapApp()
    app.mainloop()
