import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("HuggingFace Model Interface")
        self.root.geometry("1160x650")
        self.root.configure(bg="#f0f0f0")

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()