import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [reviews, setReviews] = useState([])
  const [inputText, setInputText] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 1. Ambil data review saat aplikasi dibuka pertama kali
  useEffect(() => {
    fetchReviews()
  }, [])

  const fetchReviews = async () => {
    try {
      // Panggil endpoint GET dari backend kita
      const response = await fetch('http://127.0.0.1:8000/api/reviews')
      const data = await response.json()
      setReviews(data)
    } catch (err) {
      console.error("Gagal ambil data:", err)
      setError("Gagal mengambil data. Pastikan Backend sudah jalan!")
    }
  }

  // 2. Fungsi saat tombol "Analyze" diklik
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!inputText) return

    setLoading(true)
    setError(null)

    try {
      // Kirim text ke endpoint POST backend
      const response = await fetch('http://127.0.0.1:8000/api/analyze-review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      })

      if (!response.ok) throw new Error("Gagal analisa")

      const newReview = await response.json()
      
      // Masukkan hasil baru ke paling atas list
      setReviews([newReview, ...reviews]) 
      setInputText("") // Kosongkan form input
    } catch (err) {
      console.error(err)
      setError("Terjadi kesalahan saat analisa AI.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>🤖 Product Review Analyzer</h1>
      <p>Powered by Hugging Face & Gemini</p>

      {/* --- BAGIAN FORM INPUT --- */}
      <div className="card input-section">
        <form onSubmit={handleSubmit}>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Tulis review produk di sini (Bahasa Inggris)..."
            rows="4"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !inputText}>
            {loading ? "Sedang Menganalisa..." : "Analyze Review"}
          </button>
        </form>
        {error && <p className="error-msg">{error}</p>}
      </div>

      {/* --- BAGIAN HASIL (LIST) --- */}
      <div className="results-list">
        <h2>History Analysis ({reviews.length})</h2>
        {reviews.map((review) => (
          <div key={review.id} className={`review-card ${review.sentiment}`}>
            <div className="card-header">
              <span className={`badge ${review.sentiment}`}>
                {review.sentiment}
              </span>
              <span className="date">ID: {review.id}</span>
            </div>
            
            <p className="review-text">"{review.review_text}"</p>
            
            <div className="key-points">
              <strong>✨ Key Points (Gemini):</strong>
              <div style={{whiteSpace: 'pre-line', marginTop: '5px', color: '#555'}}>
                {review.key_points}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App