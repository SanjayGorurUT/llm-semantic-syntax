import os
# API key should be set via environment variable: export GEMINI_API_KEY="your-key-here"

import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Available Gemini models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")

