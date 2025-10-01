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

