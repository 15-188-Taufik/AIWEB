from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <--- Import ini    
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Import file-file kita
import models
import database
import ai_services

# Setup Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- TAMBAHKAN BAGIAN INI (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua frontend (React) mengakses API ini
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua method (GET, POST, dll)
    allow_headers=["*"],
)
# -----------------------------------

# --- Schemas (Validasi Input/Output) ---
class ReviewInput(BaseModel):
    text: str

class ReviewResponse(BaseModel):
    id: int
    review_text: str
    sentiment: str
    key_points: str
    
    class Config:
        orm_mode = True

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Product Review Analyzer API is Ready!"}

# 1. POST: Analyze & Save Review
@app.post("/api/analyze-review", response_model=ReviewResponse)
def analyze_review(review: ReviewInput, db: Session = Depends(database.get_db)):
    
    # A. Jalankan AI Services
    # Sentiment (Sudah OK)
    sentiment_result = ai_services.analyze_sentiment(review.text)
    
    # Gemini (Kalau masih error, dia akan save pesan errornya, aplikasi tetap jalan)
    key_points_result = ai_services.extract_key_points(review.text)
    
    # B. Simpan ke Database
    new_review = models.Review(
        review_text=review.text,
        sentiment=sentiment_result,
        key_points=key_points_result
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review

# 2. GET: Get All Reviews
@app.get("/api/reviews", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(database.get_db)):
    reviews = db.query(models.Review).order_by(models.Review.id.desc()).all()
    return reviews