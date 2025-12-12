import os
import time
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_sentiment(text: str):
    # --- PERBAIKAN 1: URL BARU (ROUTER) ---
    # URL ini sesuai instruksi error log Hugging Face
    model_id = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    API_URL = f"https://router.huggingface.co/hf-inference/models/{model_id}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    print(f"[DEBUG] Analyzing Sentiment...")
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        # Jika model loading (503), tunggu sebentar
        if response.status_code == 503:
            print("[DEBUG] Model loading, waiting 3s...")
            time.sleep(3)
            response = requests.post(API_URL, headers=headers, json={"inputs": text})

        if response.status_code != 200:
            print(f"[ERROR] HF Error {response.status_code}: {response.text}")
            return "NEUTRAL"
            
        result = response.json()
        
        # Parsing hasil Roberta
        if isinstance(result, list) and len(result) > 0:
            scores = result[0]
            # Urutkan score tertinggi
            top_result = max(scores, key=lambda x: x['score'])
            label = top_result['label']
            
            # Mapping Label
            if label == "positive": return "POSITIVE"
            if label == "negative": return "NEGATIVE"
            return "NEUTRAL"
            
        return "NEUTRAL"

    except Exception as e:
        print(f"[EXCEPTION] HF: {e}")
        return "NEUTRAL"

def extract_key_points(text: str):
    print(f"[DEBUG] Extracting Key Points...")
    
    if not GEMINI_API_KEY:
        return "Error: No API Key"

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # --- PERBAIKAN 2: GANTI KE GEMINI 1.5 FLASH ---
        # Model ini adalah standar Free Tier yang paling stabil saat ini.
        # Karena librarymu sudah update, ini PASTI jalan.
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = (
            f"Summarize this product review into 3 short bullet points. "
            f"Review: '{text}'"
        )
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.replace("**", "").strip()
        else:
            return "No result from Gemini."
            
    except Exception as e:
        # Menangkap error Quota agar tidak crash
        if "429" in str(e):
            print("[ERROR] Gemini Quota Exceeded (Tunggu sebentar).")
            return "Server Busy (Quota Limit)"
        print(f"[EXCEPTION] Gemini: {e}")
        return "Failed to extract points."