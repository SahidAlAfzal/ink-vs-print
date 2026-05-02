from fastapi import FastAPI, UploadFile, File # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import shutil
import os
import ocr_engine
import similarity_meter

app = FastAPI()

# This allows your HTML file to talk to your Python server safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_documents(doc1: UploadFile = File(...), doc2: UploadFile = File(...)):
    # 1. Create a temp folder for the files
    os.makedirs("temp", exist_ok=True)
    hand_path = f"temp/{doc1.filename}"
    print_path = f"temp/{doc2.filename}"

    # 2. Save the uploaded files temporarily
    with open(hand_path, "wb") as buffer:
        shutil.copyfileobj(doc1.file, buffer)
    with open(print_path, "wb") as buffer:
        shutil.copyfileobj(doc2.file, buffer)

    try:
        # 3. Run the AI pipeline
        hand_reader = ocr_engine.HandwrittenOCR()
        print_reader = ocr_engine.PrintedOCR()

        text1 = hand_reader.extract_text(hand_path)
        text2 = print_reader.extract_text(print_path)

        results = similarity_meter.get_all_similarity(text1, text2)

        # 4. Return the data to the frontend
        return {
            "status": "success",
            "text1": text1,
            "text2": text2,
            "scores": results
        }
    finally:
        # 5. Clean up the temp files so you don't need a database!
        os.remove(hand_path)
        os.remove(print_path)