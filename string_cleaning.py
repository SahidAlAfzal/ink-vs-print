import re
import string

def normalize_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    
    text = raw_text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # The \s+ catches any whitespace (newlines, tabs, multiple spaces)
    clean_text = re.sub(r'\s+',' ',raw_text)
    return clean_text.strip()