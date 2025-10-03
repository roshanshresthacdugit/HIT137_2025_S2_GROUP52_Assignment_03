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

        self.load_sections_from_json()


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
        """
        Generates and displays a single, collapsible information section in the panel.
        """
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
    
    def open_add_window(self):
        """Opens a new dialog window to allow the user to input a title and description for a new section."""

        popup = tk.Toplevel()
        popup.title("Add Information")
        popup.geometry("400x250")
        popup.configure(bg="white")

        tk.Label(popup, text="Title:", font=("Arial", 10), bg="white").pack(anchor="w", padx=10, pady=5)
        key_entry = ttk.Entry(popup, font=("Arial", 10))
        key_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(popup, text="Description:", font=("Arial", 10), bg="white").pack(anchor="w", padx=10, pady=5)
        desc_entry = tk.Text(popup, height=4, wrap="word", font=("Arial", 10))
        desc_entry.pack(fill="x", padx=10, pady=5)

        save_btn = tk.Button(
            popup, text="Save", font=("Arial", 10), bg="#28a745", fg="white",
            command=lambda: self.save_section(key_entry, desc_entry, popup)
        )
        save_btn.pack(pady=10,ipady=5, ipadx=10)
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#218838"))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg="#28a745"))

    def save_section(self, key_entry, desc_entry, popup):
        """
        Validates input from the 'Add New Section' dialog, creates the section, 
        and updates the persistent JSON file.
        """
        key = key_entry.get().strip()
        desc = desc_entry.get("1.0", tk.END).strip()
        if key and desc:
            self.add_section(key, desc, top=True)
            self.update_json(key, desc)
            popup.destroy()
        else:
            messagebox.showwarning("Input Missing", "Please provide both a header and description.")

    def update_json(self, key, desc):
        """Update JSON file with a new section."""
        data = {}
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                pass
        data[key] = desc
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def delete_section(self, frame, title):
        """delete the section from the frame"""
        frame.destroy()
        if title in self.sections:
            del self.sections[title]
            self.remove_from_json(title)

    def remove_from_json(self, title):
        """Remove a section from JSON file."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if title in data:
                    del data[title]
                    with open(self.json_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update {self.json_file}\n{e}")
