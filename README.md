# 🤖 Product Review Analyzer

Aplikasi web untuk menganalisis ulasan produk secara otomatis menggunakan Kecerdasan Buatan (AI). Aplikasi ini dapat menentukan sentimen (Positif/Negatif/Netral) dan merangkum poin-poin penting dari ulasan panjang.

## 🚀 Fitur Utama
* **Sentiment Analysis:** Menggunakan Hugging Face (Model Roberta) untuk mendeteksi emosi ulasan.
* **Key Points Extraction:** Menggunakan Google Gemini AI untuk merangkum ulasan menjadi bullet points.
* **Database Integration:** Menyimpan semua hasil analisis ke PostgreSQL (NeonDB).
* **Interactive UI:** Tampilan modern menggunakan React + Vite.

## 🛠️ Tech Stack
* **Frontend:** React.js, Vite, CSS Native.
* **Backend:** Python FastAPI.
* **Database:** PostgreSQL (via NeonDB & SQLAlchemy).
* **AI Services:** Hugging Face API, Google Gemini API.

## 📂 Struktur Project
```text
product-review-analyzer/
├── backend/            # API Server (FastAPI)
│   ├── main.py         # Entry point & Endpoints
│   ├── database.py     # Koneksi Database
│   ├── models.py       # Schema Database
│   ├── ai_services.py  # Logika AI (Hugging Face & Gemini)
│   └── requirements.txt
└── frontend/           # User Interface (React)
    ├── src/
    │   ├── App.jsx     # Logic Frontend
    │   └── App.css     # Styling
    └── package.json
```

## ⚙️ Cara Menjalankan (Installation)
1. Setup Backend
Masuk ke folder backend, buat virtual environment, dan install dependencies.

```bash
cd backend
python -m venv venv
# Aktifkan venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
Buat file .env di dalam folder backend dan isi dengan konfigurasi berikut:
```bash
DATABASE_URL=postgresql://user:pass@host/db_name
HUGGINGFACE_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
```

Jalankan server:

```
uvicorn main:app --reload

```
