import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# ==================== CONFIGURATION ====================
class Config:
    DPI = 300
    # Mac users with Homebrew don't need paths. 
    # Windows users would set this: pytesseract.pytesseract.tesseract_cmd = r'C:\...'

# ==================== HANDWRITTEN OCR ====================
class HandwrittenOCR:
    def __init__(self):
        print("Initializing Tesseract for Handwriting...")

    def preprocess(self, img_pil):
        """Heavy OpenCV filtering to make handwriting legible to Tesseract"""
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # 1. Blur to smooth out messy pen strokes
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 2. Adaptive Threshold (handles uneven lighting/phone shadows beautifully)
        binary = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5
        )
        
        # 3. Morphological Erode (Thickens the black ink slightly)
        kernel = np.ones((2, 2), np.uint8)
        thick_text = cv2.erode(binary, kernel, iterations=1)
        
        return Image.fromarray(thick_text)

    def extract_text(self, file_path):
        print(f"\n--- HANDWRITTEN OCR: {file_path} ---")

        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path, dpi=Config.DPI)
        else:
            images = [Image.open(file_path)]

        full_text = ""
        for i, img in enumerate(images):
            processed = self.preprocess(img)
            # psm 6 assumes a single uniform block of text. Great for handwritten paragraphs.
            text = pytesseract.image_to_string(processed, config='--psm 6')
            full_text += text + "\n"

        return full_text.strip()


# ==================== PRINTED OCR ====================
class PrintedOCR:
    def __init__(self):
        print("Initializing Tesseract for Printed Text...")

    def preprocess(self, img_pil):
        """Standard filtering for clean printed text"""
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Standard Otsu's thresholding for perfectly black/white printed text
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return Image.fromarray(binary)

    def extract_text(self, file_path):
        print(f"\n--- PRINTED OCR: {file_path} ---")

        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path, dpi=Config.DPI)
        else:
            images = [Image.open(file_path)]

        full_text = ""
        for i, img in enumerate(images):
            processed = self.preprocess(img)
            text = pytesseract.image_to_string(processed, config='--psm 6')
            full_text += text + "\n"

        return full_text.strip()