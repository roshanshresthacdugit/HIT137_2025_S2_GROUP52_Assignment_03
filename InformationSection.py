import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

class InformationSection:
    def __init__(self, parent, model_use_frame=None, json_file="information_text.json"):
        self.model_use_frame = model_use_frame
        self.json_file = json_file
        self.sections = {}

        panel = tk.Frame(parent, bg="white", bd=1, relief="solid")
        panel.place(x=740, y=0, width=400, height=600)

        tk.Label(panel, text="Information Sections", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

        add_btn = tk.Button(
            panel, text="+ Add Information", font=("Arial", 10), bg="#007bff", fg="white", relief="flat",
            command=self.open_add_window
        )
        add_btn.pack(fill="x", padx=10, pady=5)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#0056b3"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#007bff"))

        # Scrollable area
        self.canvas = tk.Canvas(panel, bg="white", highlightthickness=0, width=20)
        self.scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=300)
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", lambda e: self.set_scroll_active(True))
        self.canvas.bind("<Leave>", lambda e: self.set_scroll_active(False))
        self.scroll_frame.bind("<Enter>", lambda e: self.set_scroll_active(True))
        self.scroll_frame.bind("<Leave>", lambda e: self.set_scroll_active(False))

    def set_scroll_active(self, active):
        if self.model_use_frame:
            self.model_use_frame.set_right_panel_active(active)
        if active:
            self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        else:
            self.canvas.unbind("<MouseWheel>")
 
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
        
    def load_sections_from_json(self):
        """Load sections from JSON file."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for title, desc in data.items():
                        self.add_section(title, desc, top=False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {self.json_file}\n{e}")
        else:
            messagebox.showwarning("File Missing", f"{self.json_file} not found.")
 
    def add_section(self, title, desc, top=True):
        frame = tk.Frame(self.scroll_frame, bg="white", bd=1, relief="raised")
        header_frame = tk.Frame(frame, bg="white")
        header_frame.pack(fill="x")
 
        tk.Label(header_frame, text=title, font=("Arial", 11, "bold"), bg="white", anchor="w").pack(side="left", padx=5, pady=4)
 
        del_btn = tk.Button(
            header_frame, text="❌", font=("Arial", 10), bg="white", fg="#ff4d4d", bd=0,
            command=lambda f=frame, t=title: self.delete_section(f, t)
        )
        del_btn.pack(side="right", padx=5)
        del_btn.bind("<Enter>", lambda e: del_btn.config(fg="#cc0000"))
        del_btn.bind("<Leave>", lambda e: del_btn.config(fg="#ff4d4d"))
 
        text_label = tk.Label(frame, text=desc, font=("Arial", 10), wraplength=320, justify="left", bg="white")
        text_label.pack(anchor="w", padx=10, pady=5)
 
        if top and self.scroll_frame.winfo_children():
            frame.pack(fill="x", padx=10, pady=5, before=self.scroll_frame.winfo_children()[0])
        else:
            frame.pack(fill="x", padx=10, pady=5)
 
        self.sections[title] = frame