# ink-vs-print
# 📄 AI Document Similarity Analyzer

An intelligent Python pipeline designed to extract text from physical/digital documents (handwritten and printed) and evaluate their structural, lexical, and semantic similarity using state-of-the-art Optical Character Recognition (OCR) and Natural Language Processing (NLP).

## 🚀 Features

* **Handwritten OCR (TrOCR):** Utilizes Microsoft's Transformer-based `trocr-base-handwritten` model to interpret difficult cursive and handwritten text.
* **Printed OCR (Tesseract):** Uses industry-standard `pytesseract` for highly accurate printed text extraction.
* **Aggressive Text Normalization:** Cleans formatting, casing, and punctuation to ensure similarity metrics are not skewed by OCR formatting errors.
* **Tri-Factor Similarity Engine:**
  * **Structural (Edit Similarity):** Character-by-character typo detection via `difflib`.
  * **Lexical (TF-IDF):** Vocabulary overlap analysis using `scikit-learn`.
  * **Semantic (Embeddings):** Contextual meaning comparison using HuggingFace's `all-MiniLM-L6-v2` transformer model.
* **Interactive Web UI:** Includes a drag-and-drop web application built with Streamlit.

---

## 🛠️ Prerequisites & System Requirements

Before running the application, you must install the underlying OCR engines on your operating system.

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

1. Clone or download the repository to your local machine.
2. Navigate to the project directory in your terminal:

```bash
cd path/to/your/project
```

3. (Optional but Recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

4. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

> **Note:** The first time you run the application, it will automatically download the TrOCR and SentenceTransformer models from HuggingFace (approx. 1.5GB).

---

## 💻 Usage

This project to run the analysis: an interactive web application or a command-line interface.

### Command Line Interface

Run the pipeline directly in your terminal.

```bash
python main.py
```

> **Note:** To test via CLI, ensure your test files are correctly referenced inside `main.py` (e.g., pointing to the files in the `input/` directory).