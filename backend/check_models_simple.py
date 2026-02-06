import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    with open("simple_models.txt", "w", encoding="utf-8") as f:
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
                found = True
        if not found:
            f.write("No models found.\n")
except Exception as e:
    with open("simple_models.txt", "w", encoding="utf-8") as f:
        f.write(f"Error: {str(e)}\n")
