import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util # type: ignore
from string_cleaning import normalize_text


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model is loaded successfully!")

# Structural (characters)
def get_edit_similarity(text1:str ,text2:str) -> float:
    # If both are empty. They match completely so identical = 1.0
    if not text1 and not text2:
        return 1.0
    
    """The basic idea is to find the longest contiguous
    matching subsequence that contains no "junk" elements"""
    
    # obj = difflib.SequenceMatcher(None,text1,text2)
    # print(obj)
    return difflib.SequenceMatcher(None,text1,text2).ratio()   # Return a measure of the sequences' similarity (float in [0,1])



# Lexical (Vocabulary)
def get_tfidf_similarity(text1:str ,text2:str) -> float:
    if not text1 or not text2:
        return 0.0
    
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([text1,text2])   # sparse matrix, direct cosine calc wont work
        cos = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2]) # expects input vector in 2D
        # print(cos)
        return float(cos[0][0])
    
    except ValueError:
        # Handles edge cases where text might be just stop-words or empty
        return 0.0
    

# Semantic (Meaning)
def get_embedding_similarity(text1:str ,text2:str) -> float:
    if not text1 or not text2:
        return 0.0
    
    vec1 = embedding_model.encode(text1)
    vec2 = embedding_model.encode(text2)
    
    cosine_val = util.cos_sim(vec1,vec2).item()
    
    return float(cosine_val)
    
    
    
def get_all_similarity(raw_text1:str, raw_text2:str):
    text1 = normalize_text(raw_text1)
    text2 = normalize_text(raw_text2)
    
    
    print(f"\n[DEBUG] Normalized Hand: '{text1}'")
    print(f"[DEBUG] Normalized Print: '{text2}'\n")
    
    edit_score = get_edit_similarity(text1, text2)
    tfidf_score = get_tfidf_similarity(text1, text2)
    embedding_score = get_embedding_similarity(text1, text2)
    
    final_score = (edit_score + tfidf_score + embedding_score) / 3
    
    
    return {
        "edit_similarity": round(edit_score, 4),
        "tfidf_similarity": round(tfidf_score, 4),
        "embedding_similarity": round(embedding_score, 4),
        "final_normalized_score": round(final_score, 4)
    }

if __name__ == "__main__":
    printed = " The quick brown fox jumps over the lazy dog."
    handwritten_ocr = "The qu1ck br0wn f0x jumpz over the lazy dog. " # OCR messed up

    with open("output/printed.txt","r") as pfile:
        text1 = pfile.read()
    
    with open("output/handwritten.txt","r") as hfile:
        text2 = hfile.read()

    # print(get_edit_similarity(printed,handwritten_ocr))
    print(get_edit_similarity(text1,text2))
    print(get_tfidf_similarity(text1,text2))
    print(get_embedding_similarity(text1,text2))
    
    print("-" * 15)
    print(get_all_similarity(text1,text2))


