import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key tidak ditemukan di .env")
else:
    print(f"✅ API Key ditemukan: {api_key[:5]}...")
    genai.configure(api_key=api_key)
    
    print("\n🔍 Sedang mencari model Gemini yang tersedia untukmu...")
    try:
        # List semua model
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - Model Tersedia: {m.name}")
    except Exception as e:
        print(f"❌ Error koneksi: {e}")