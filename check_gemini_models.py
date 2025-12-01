import os
os.environ['GEMINI_API_KEY'] = "AIzaSyD_1pSTy7EohE7zMz_qEGoYlCl4V2buZFQ"

import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Available Gemini models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")

