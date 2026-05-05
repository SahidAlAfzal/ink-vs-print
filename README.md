Readme · MD
Copy

# 📄 AI Document Similarity API
 
A high-performance REST API designed to extract, normalize, and mathematically compare the semantic and structural similarity between physical handwritten documents and printed digital files.
 
## 🚀 System Architecture
 
This project is divided into two primary micro-engines:
 
### 1. "The Eyes" (Vision & OCR Pipeline)
 
We utilize heavily optimized OpenCV pre-processing combined with **Tesseract OCR** to handle both standard printed text and messy handwriting.
 
> **Note on Architecture:** During development, Transformer-based models (like TrOCR) were evaluated but discarded due to high latency and "hallucinations" (inventing non-existent words on poor crops). Tesseract provides a deterministic, lightweight extraction base that our NLP engine is specifically designed to correct and grade.
 
### 2. "The Brain" (Tri-Factor NLP Engine)
 
Extracted text is aggressively normalized (stripping artifacts, standardizing whitespace/casing) before passing through a custom scoring matrix:
 
- **Structural (Edit Similarity):** Uses `difflib` to catch character-level typos and layout shifts.
- **Lexical (TF-IDF):** Uses `scikit-learn` Cosine Similarity to measure exact vocabulary overlap while penalizing common stop-words.
- **Semantic (Embeddings):** Uses HuggingFace's `all-MiniLM-L6-v2` neural network to map sentences into 384-dimensional vectors, understanding the *context* of the document even if the OCR misspelled words.
**The Master Equation:**
 
To account for standard handwriting OCR noise, the final score is a weighted average prioritizing lexical and semantic meaning over exact character matches:
 
```
Final Score = (Edit + 2 * TF-IDF + 2 * Embedding) / 5
```
 
---
 
## 🛠️ Prerequisites & System Requirements
 
Before running the API, you must install the underlying OCR engine on your operating system.
 
**For macOS (Using Homebrew):**
 
```bash
brew install tesseract
brew install poppler
```
 
**For Windows:**
 
1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your system PATH.
2. Install [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) and add the `bin` folder to your system PATH.
---
 
## 📦 Installation
 
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/document-similarity-api.git
   cd document-similarity-api
   ```
 
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
 
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
 
   > *Note: The first run will automatically download the `all-MiniLM-L6-v2` model from HuggingFace.*
---
 
## 💻 Usage & Live Demo
 
This application is built using **FastAPI**. It includes a built-in, interactive Swagger UI dashboard for testing the endpoints without needing a separate frontend.
 
1. **Start the API server:**
   ```bash
   uvicorn api:app --reload
   ```
 
2. **Access the Interface:**
   Open your web browser and navigate to:
   👉 **`http://127.0.0.1:8000/docs`**
3. **Run a Test:**
   - Click on the green `POST /analyze` endpoint.
   - Click the **"Try it out"** button.
   - Upload your handwritten test image to `doc1` and your printed test document to `doc2`.
   - Click **Execute** to view the extracted text and the final similarity math in real-time.
---
