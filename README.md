software now assignment 3

Team Member
<br> 
Roshan Kumar Shrestha(S395498) 
<br>Subash Gaire(S393152) 
<br>Sujal Bhandari(S392965) 
<br>Aaron Madelo(S389992)

Hugging Face AI Model Interface
<br>A Python desktop application using Tkinter to provide a simple, user-friendly GUI for interacting with various AI models from the Hugging Face Hub. The app supports chat, text-to-image, text-to-video, and image classification models in an intuitive chat-like interface.

Core Features
<br>Multi-Model Support: Easily switch between Chat LLMs, Text-to-Image, Text-to-Video, and Image Classification models.

Secure Token Authentication: A startup prompt securely requests and validates your Hugging Face access token.

Interactive Chat UI: Send text prompts, upload images, and receive responses, all within a single, scrollable chat window.

Dynamic Information Panel: A customizable side panel to add, view, and delete notes, with content saved to a JSON file.


Quick Start
Clone the Repository

```
git clone <your-repository-url>
cd <your-repository-directory>

```
Requirements
All required Python packages are listed in the requirements.txt file.

Install Dependencies
```
pip install -r requirements.txt
```
```
python MainWindow.py
First-Time Use
Enter your Hugging Face access token.
Select a model from the dropdown in the left panel and click Use Model.
Start sending prompts or uploading files in the center panel.
```

Supported Models
The application is pre-configured to support the following models:


| Model Name                        | Type                  | Hugging Face ID              | 
| -----                             | -----                 | -----                        |      
| DeepSeek-V3 (Chat LLM)            | Chat                  | deepseek-ai/DeepSeek-V3-0324 | 
| FLUX.1-dev (Text-to-Image)        | Text-to-Image         | black-forest-labs/FLUX.1-dev | 
| Wan2.2-T2V-A14B (Text-to-Video)   | Text-to-Video         | Wan-AI/Wan2.2-T2V-A14B       | 
| ViT (Image Classification)        | Image Classification  | google/vit-base-patch16-224  | 
