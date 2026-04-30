import os
import ocr_engine     
import similarity_meter   

def run_full_pipeline(handwritten_path, printed_path):
    print("\n" + "="*50)
    print("STARTING AI DOCUMENT PIPELINE")
    print("="*50)

    # 1. Wake up the OCR engines (This will load the Microsoft model into memory)
    print("\n[SYSTEM] Loading AI Models...")
    hand_reader = ocr_engine.HandwrittenOCR()
    print_reader = ocr_engine.PrintedOCR()

    # 2. Extract the text
    print("\n[PHASE 1] Extracting text from Handwritten Document...")
    text_handwritten = hand_reader.extract_text(handwritten_path)
    
    print("\n[PHASE 2] Extracting text from Printed Document...")
    text_printed = print_reader.extract_text(printed_path)

    # 3. Pass the text to your Brain
    print("\n[PHASE 3] Running Similarity Analysis...")
    results = similarity_meter.get_all_similarity(text_handwritten, text_printed)

    # 4. Print the final grade
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    print("-" * 50)
    print(f"Edit Similarity (Typos/Structure):  {results['edit_similarity']}")
    print(f"TF-IDF Similarity (Vocabulary):     {results['tfidf_similarity']}")
    print(f"Embedding Similarity (Meaning):     {results['embedding_similarity']}")
    print("-" * 50)
    print(f"FINAL NORMALIZED SCORE (0 to 1):    {results['final_normalized_score']}")
    print("="*50)

if __name__ == "__main__":
    # Point these to the files you want to test
    # (Make sure these match your actual computer's paths)
    test_handwritten = "input/handwritten.pdf" 
    test_printed = "input/printed_format.pdf"
    
    if os.path.exists(test_handwritten) and os.path.exists(test_printed):
        run_full_pipeline(test_handwritten, test_printed)
    else:
        print("Error: Could not find the test files. Please check your paths.")