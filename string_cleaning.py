import re

def normalize_text(raw_text: str) -> str:
    """
    Aggressively cleans OCR text to prevent formatting/artifact penalties.
    Keeps ONLY: English letters, numbers, full stops, commas, and spaces.
    """
    if not raw_text:
        return ""
    
    # Step 1: Remove EVERYTHING except a-z, A-Z, 0-9, periods (.), commas (,), and whitespace (\s)
    # The ^ symbol inside the brackets means "NOT". 
    clean_text = re.sub(r'[^a-zA-Z0-9.,\s]', '', raw_text)
    
    # Step 2: Catch all newlines (\n), tabs (\t), and multiple spaces, and crush them into one single space
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # Step 3: (Optional but recommended) Force lowercase so "The" and "the" match perfectly
    clean_text = clean_text.lower()
    
    # Step 4: Remove any accidental spaces at the very beginning or end
    return clean_text.strip()

# --- Quick Test ---
if __name__ == "__main__":
    messy_ocr_output = "The feline   jumped \n\n >> over the «lazy» dog?! | 100%"
    print(f"Before: {messy_ocr_output}")
    print(f"After:  {normalize_text(messy_ocr_output)}")