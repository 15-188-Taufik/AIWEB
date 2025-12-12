import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"🔑 Memeriksa API Key: {api_key[:5]}... (OK)")

genai.configure(api_key=api_key)

# Daftar model yang akan kita coba (berdasarkan list kamu tadi)
candidate_models = [
    "gemini-2.0-flash",       # Percobaan 1
    "models/gemini-2.0-flash", # Percobaan 2 (pakai prefix)
    "gemini-pro",             # Percobaan 3 (standar)
    "gemini-1.5-flash"        # Percobaan 4
]

prompt = "Hello, are you working?"

print("\n🚀 MEMULAI TEST KONEKSI GEMINI...")

success = False

for model_name in candidate_models:
    print(f"\n-------------------------------------")
    print(f"👉 Mencoba Model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        
        if response.text:
            print(f"✅ SUKSES! Model '{model_name}' berhasil merespon.")
            print(f"📝 Respon: {response.text}")
            success = True
            break # Berhenti jika sudah berhasil
            
    except Exception as e:
        print(f"❌ GAGAL. Error: {e}")

if not success:
    print("\n😭 Semua percobaan gagal. Mohon copy-paste pesan error di atas ke chat.")