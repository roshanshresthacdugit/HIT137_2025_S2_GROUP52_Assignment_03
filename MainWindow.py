import tkinter as tk
from ModelConfiguration import ModelConfiguration
from ModelUse import ModelUse 
from InformationSection import InformationSection

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("HuggingFace Model Interface")
        self.root.geometry("1160x650")
        self.root.configure(bg="#f0f0f0")

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Panels
        self.model_config_frame = ModelConfiguration(main_frame)
        self.model_use_frame = ModelUse(main_frame, self.model_config_frame)
        self.info_frame = InformationSection(main_frame, self.model_use_frame)

        # Ensure main window stays in focus
        self.root.focus_force()
        self.root.lift()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()