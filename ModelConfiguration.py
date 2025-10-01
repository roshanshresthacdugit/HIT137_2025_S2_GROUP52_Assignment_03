import json
import re
import requests
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from huggingface_hub import InferenceClient, InferenceTimeoutError


class ModelConfiguration:
    def __init__(self, parent):
        self.parent = parent  
        self.selected_model_id = None
        self.model_type = None
        self.client = None

        ########## Ask for Hugging Face access token ###############
        self.set_token(initial=True)

        ######## making panel frame #############
        panel = tk.Frame(parent, bg="white", bd=1, relief="solid")
        panel.place(x=0, y=0, width=300, height=600)

        tk.Label(panel, text="Model Configuration", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=10)


        #### Making Token Button for user if not entered while opening application #######
        set_token_btn = tk.Button(
            panel, text="Set Token", bg="#007bff", fg="white", relief="flat",
            command=lambda: self.set_token(initial=False)
        )
        set_token_btn.pack(fill="x", padx=10, pady=5)
        set_token_btn.bind("<Enter>", lambda e: set_token_btn.config(bg="#0056b3"))
        set_token_btn.bind("<Leave>", lambda e: set_token_btn.config(bg="#007bff"))


        ############## Model Selection menu and loading buttons ###################
        tk.Label(panel, text="Select Model:", bg="white").pack(anchor="w", padx=10)
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(
            panel,
            textvariable=self.model_var,
            state="readonly",
            values=[
                "DeepSeek-V3 (Chat LLM)",
                "FLUX.1-dev (Text-to-Image)",
                "Wan2.2-T2V-A14B (Text-to-Video)",
                "ViT (Image Classification)",
            ],
        )
        self.model_dropdown.current(0)
        self.model_dropdown.pack(fill="x", padx=10, pady=5)

        load_btn = tk.Button(panel, text="Use Model", bg="green", fg="white", relief="flat",
                             command=self.load_model)
        load_btn.pack(fill="x", padx=10, pady=10)

        self.info_frame = tk.LabelFrame(panel, text="Model Information", bg="white")
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_label = tk.Label(self.info_frame, text="Status: Not Loaded", anchor="w", bg="white")
        self.status_label.pack(fill="x")

        self.type_label = tk.Label(self.info_frame, text="Type: -", anchor="w", bg="white")
        self.type_label.pack(fill="x")

        self.desc_label = tk.Label(self.info_frame, text="Select a model to see details.", wraplength=250, anchor="w", bg="white", justify="left")
        self.desc_label.pack(fill="x", pady=5)

        with open("models_info.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.models = {name: info["id"] for name, info in data.items()}
        self.model_descriptions = {name: info["description"] for name, info in data.items()} 
        

    def set_token(self, initial=False):
        pass


    def load_model(self):
        pass
    

    def run_inference(self, prompt, image_path=None):
        if not self.client:
            raise RuntimeError("No valid Hugging Face token provided. Please use 'Set Token Button' to enter a valid token.")
        if not self.selected_model_id:
            raise RuntimeError("No model selected")

        try:
            if "Chat LLM" in self.model_type:
                response = self.client.chat.completions.create(
                    model=self.selected_model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                return response.choices[0].message.content

            elif "Text-to-Image" in self.model_type:
                image = self.client.text_to_image(
                    model=self.selected_model_id,
                    prompt=prompt
                )
                return image  # PIL.Image

            elif "Text-to-Video" in self.model_type:
                video_bytes = self.client.text_to_video(
                    model=self.selected_model_id,
                    prompt=prompt
                )
                with open("output_video.mp4", "wb") as f:
                    f.write(video_bytes)
                messagebox.showinfo("successfull","video saved as ouput_video.mp4")
                return "Video saved as output_video.mp4"

            elif "Image Classification" in self.model_type:
                if not image_path:
                    raise RuntimeError("Image path required for Image Classification. Please upload a valid .jpg, .jpeg, or .png file.")
                try:
                    result = self.client.image_classification(
                        image=image_path,
                        model=self.selected_model_id
                    )
                    # Fallback to resnet-50 if vit fails
                    if not result or not isinstance(result, list) or 'label' not in result[0]:
                        fallback_model = "microsoft/resnet-50"
                        result = self.client.image_classification(
                            image=image_path,
                            model=fallback_model
                        )
                        if not result or not isinstance(result, list) or 'label' not in result[0]:
                            raise ValueError("Both primary and fallback models failed to classify the image.")
                    top_pred = result[0]
                    return f"Class: {top_pred['label']} (Confidence: {top_pred['score']:.2%})"
                except ValueError as ve:
                    raise RuntimeError(f"Image Classification failed: Invalid model response - {str(ve)}")
                except Exception as e:
                    raise RuntimeError(f"Image Classification failed: {str(e)}. Ensure the image path is valid and the model is accessible.")

            else:
                return "Unsupported model type"

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RuntimeError("Rate limit exceeded. Please try again later or check your subscription.")
            raise RuntimeError(f"API Error: {str(e)}")
        except InferenceTimeoutError:
            raise RuntimeError("Inference request timed out. Please try again.")
        except Exception as e:
            raise RuntimeError(f"Error during inference: {str(e)}")