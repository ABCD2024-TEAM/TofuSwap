#Template for the application
import tkinter as tk
from tkinter import ttk, messagebox

class TofuSwapApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("TofuSwap")
        self.geometry("500x400")
        self.configure(bg="#f7f2e7")  # Light beige background

        # Title label
        title_label = tk.Label(self, text="TofuSwap", font=("Segoe UI", 20, "bold"), fg="#2e7d32", bg="#f7f2e7")
        title_label.pack(pady=20)

        # Input field
        self.input_var = tk.StringVar()
        input_frame = tk.Frame(self, bg="#f7f2e7")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Chinese Dish:", font=("Segoe UI", 12), bg="#f7f2e7").pack(side=tk.LEFT)
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=30)
        input_entry.pack(side=tk.LEFT, padx=5)

        # Search button
        search_button = ttk.Button(self, text="Find Veggie Swap", command=self.find_swap)
        search_button.pack(pady=10)

        # Results area
        self.result_text = tk.Text(self, wrap="word", height=10, width=50, font=("Segoe UI", 10))
        self.result_text.pack(pady=10)

        # Quit button
        quit_button = ttk.Button(self, text="Exit", command=self.quit)
        quit_button.pack(pady=10)

    def find_swap(self):
        dish = self.input_var.get().strip()
        if not dish:
            messagebox.showwarning("Input Needed", "Please enter a dish name.")
            return

        # Placeholder substitution logic
        substitutions = {
            "Kung Pao Chicken": "Kung Pao Tofu",
            "Sweet and Sour Pork": "Sweet and Sour Jackfruit",
            "Beef Chow Mein": "Mushroom Chow Mein"
        }

        veggie_version = substitutions.get(dish, f"No direct swap found for '{dish}', try tofu or seitan as a base.")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, veggie_version)

if __name__ == "__main__":
    app = TofuSwapApp()
    app.mainloop()
