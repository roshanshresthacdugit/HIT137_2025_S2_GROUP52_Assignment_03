import os
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox

class ModelUse:
    def __init__(self, parent, model_config_panel):
        self.model_config_panel = model_config_panel
        self.loaded_image = None
        self.file_path = None
        self.chat_messages = [] 
        self.is_right_panel_active = False
        self.file_label = None  

        panel = tk.Frame(parent, bg="white", bd=1, relief="solid")
        panel.place(x=310, y=0, width=420, height=600)

        tk.Label(panel, text="Chat with Model", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

        ########## Clear button ####################
        clear_btn = tk.Button(panel, text="Clear Chat", bg="#ff4d4d", fg="white", relief="flat",
                              command=self.clear_chat, font=("Arial", 10))
        clear_btn.pack(anchor="e", padx=10, pady=2)

        output_frame = tk.Frame(panel, bg="#f8f9fa", height=400)
        output_frame.pack(fill="x", padx=10, pady=10)
        output_frame.pack_propagate(False)

        ########## Output Section ###################
        self.canvas = tk.Canvas(output_frame, bg="#f8f9fa", highlightthickness=0, height=400)
        self.scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.canvas.yview)
        self.chat_frame = tk.Frame(self.canvas, bg="#f8f9fa")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        ############## Mouse wheel bindings for chat canvas#################
        self.canvas.bind("<Enter>", lambda e: self.set_model_use_panel(True))
        self.canvas.bind("<Leave>", lambda e: self.set_model_use_panel(False))
        self.chat_frame.bind("<Enter>", lambda e: self.set_model_use_panel(True))
        self.chat_frame.bind("<Leave>", lambda e: self.set_model_use_panel(False))
    

        ########### Input section ######### 
        input_frame = tk.Frame(panel, bg="#f0f0f0", height=100, bd=2, relief="groove")
        input_frame.pack(fill="x", padx=10, pady=10)
        input_frame.pack_propagate(False)

        # Input type dropdown
        main_controls_frame = tk.Frame(input_frame, bg="#f0f0f0")
        main_controls_frame.pack(side="top", fill="x", padx=5, pady=5)

        self.input_type_var = tk.StringVar()
        self.input_type_dropdown = ttk.Combobox(
            main_controls_frame,
            textvariable=self.input_type_var,
            state="readonly",
            values=["Text", "Image"],
            width=6
        )
        self.input_type_dropdown.current(0)
        self.input_type_dropdown.pack(side="left", padx=(0, 5))
        self.input_type_dropdown.bind("<<ComboboxSelected>>", self.clear_file_preview)

        #######File upload '+' button ###########
        self.file_btn = tk.Button(
            main_controls_frame,
            text="+", font=("Arial", 14, "bold"), bg="#e0e0e0", fg="#333", bd=1, relief="solid",
            command=self.upload_file
        )
        self.file_btn.pack(side="left", padx=5)

        ####### Send button#############
        self.send_btn = tk.Button(
            main_controls_frame, text="➤", font=("Arial", 12, "bold"), bg="#007bff", fg="white", bd=0,
            command=self.process_input
        )
        self.send_btn.pack(side="right", padx=(5, 0))
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg="#0056b3"))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(bg="#007bff"))
        
        #### Text Input #########
       
        self.input_entry = tk.Entry(
            main_controls_frame,
            font=("Arial", 12),
            bg="white",
            relief="flat",
            bd=1,
            highlightcolor="#4A90E2",
            highlightthickness=2,
            highlightbackground='gray'
        )
        self.input_entry.insert(0, "Type your prompt here...")
        self.input_entry.config(fg="gray")
        self.input_entry.bind("<FocusIn>", self.clear_placeholder)
        self.input_entry.bind("<KeyPress>", self.clear_placeholder_on_keypress)
        self.input_entry.bind("<FocusOut>", self.add_placeholder)
        self.input_entry.bind("<Return>", lambda e: self.process_input())
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8) 


        ### Section for the file preview ###
        self.file_preview_frame = tk.Frame(input_frame, bg="#f0f0f0")
        self.file_preview_frame.pack(side="top", fill="x", padx=5, pady=2)

        self.input_entry.focus_set()

    
    def upload_file(self):
        pass

    def process_input(self):
        sel_model = self.model_config_panel.model_type
        if not sel_model:
            messagebox.showwarning("No Model", "Please select and load a model first.")
            return

        prompt = self.input_entry.get().strip()
        if prompt == "Type your prompt here...":
            prompt = ""

        input_type = self.input_type_var.get()

        if "Chat LLM" in sel_model :
            if not prompt:
                messagebox.showwarning("Input Missing", "Please enter a text prompt.")
                return
            file_path = None
        elif "Text-to-Video" in sel_model or "Text-to-Image" in sel_model:
            if not prompt:
                messagebox.showwarning("Input Missing", "Please enter a text prompt.")
                return
            file_path = None
            messagebox.showinfo("Be patient", "Please be patient it may take a while")
        elif "Image Classification" in sel_model:
            if input_type != "Image":
                messagebox.showwarning("Invalid Input", "Select Image input type for this model.")
                return
            if not self.file_path:
                messagebox.showwarning("Input Missing", "Please upload an image for Image Classification.")
                return
            file_path = self.file_path
            self.add_chat_message(f"Uploaded Image: {os.path.basename(self.file_path)}", is_user=True, image=self.loaded_image)
        else:
            return

        ####Display user prompt in chat 
        if prompt:
            self.add_chat_message(prompt, is_user=True)

        parent = self.input_entry.winfo_toplevel()
        parent.update()

        try:
            result = self.model_config_panel.run_inference(prompt, image_path=file_path)

            if isinstance(result, Image.Image):
                img = result.resize((200, 200))
                photo = ImageTk.PhotoImage(img)
                self.add_chat_message("Generated Image", is_user=False, image=photo)
            else:
                self.add_chat_message(result, is_user=False)

            ####Clear input after successful processing
            self.input_entry.delete(0, tk.END)
            self.add_placeholder(None)
            self.clear_file_preview(None)

        except Exception as e:
            self.add_chat_message(f"Error: {e}", is_user=False, error=True)
      