import os
import torch # type: ignore
import cv2 # type: ignore
import numpy as np # type: ignore
from pdf2image import convert_from_path # type: ignore
from transformers import TrOCRProcessor, VisionEncoderDecoderModel # type: ignore
from PIL import Image # type: ignore
import pytesseract # type: ignore

# ==================== CONFIGURATION ====================
class Config:
    HANDWRITTEN_DOC = "input/handwritten.pdf"
    PRINTED_DOC = "input/printed_format.pdf"

    OUTPUT_HANDWRITTEN = "output/handwritten.txt"
    OUTPUT_PRINTED = "output/printed.txt"

    DPI = 300
    # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

    # Not needed on Mac
    POPPLER_PATH = None
    TESSERACT_PATH = None


# # Set Tesseract path
# pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH

# ==================== HANDWRITTEN OCR ====================
class HandwrittenOCR:
    def __init__(self):
        print(f"Initializing TrOCR on {Config.DEVICE}...")
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        self.model.to(Config.DEVICE)
        self.model.eval()
        print("TrOCR loaded successfully!")

    def detect_lines(self, img):
        img_array = np.array(img.convert('L'))

        _, binary = cv2.threshold(img_array, 0, 255,
                                 cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        h_projection = np.sum(binary, axis=1)
        threshold = np.mean(h_projection) * 0.3

        lines = []
        in_line = False
        start = 0

        for i, val in enumerate(h_projection):
            if not in_line and val > threshold:
                start = i
                in_line = True
            elif in_line and val <= threshold:
                if i - start > 10:
                    lines.append((start, i))
                in_line = False

        if in_line:
            lines.append((start, len(h_projection)))

        return lines

    def preprocess_line(self, img):
        img_array = np.array(img)

        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array

        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        binary = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            15, 10
        )

        kernel = np.ones((1, 2), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)

        return Image.fromarray(dilated).convert("RGB")

    def ocr_line(self, line_img):
        try:
            w, h = line_img.size
            new_width = int(w * 96 / h)
            line_img = line_img.resize((new_width, 96))

            pixel_values = self.processor(
                images=line_img,
                return_tensors="pt"
            ).pixel_values.to(Config.DEVICE)

            with torch.no_grad():
                generated_ids = self.model.generate(
                    pixel_values,
                    max_length=128,
                    num_beams=5
                )

            text = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0]

            return text.strip()

        except Exception as e:
            print(f"[OCR ERROR] {e}")
            return ""

    def extract_text(self, file_path):
        print(f"\n--- HANDWRITTEN OCR: {file_path} ---")

        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(
                file_path,
                dpi=Config.DPI
                #poppler_path=Config.POPPLER_PATH
            )
        else:
            images = [Image.open(file_path)]

        full_text = ""

        for page_no, img in enumerate(images):
            print(f"\nPage {page_no + 1}")

            lines = self.detect_lines(img)
            page_text = []

            for top, bottom in lines:
                line_img = img.crop((0, top, img.size[0], bottom))
                line_img = self.preprocess_line(line_img)

                text = self.ocr_line(line_img)
                if text:
                    page_text.append(text)

            full_text += " ".join(page_text) + "\n"

        return full_text.strip()


# ==================== PRINTED OCR ====================
class PrintedOCR:
    def __init__(self):
        print("Initializing Tesseract...")
        print("Version:", pytesseract.get_tesseract_version())

    def preprocess(self, img):
        gray = np.array(img.convert('L'))

        _, binary = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        denoised = cv2.fastNlMeansDenoising(binary, h=10)

        return Image.fromarray(denoised)

    def extract_text(self, file_path):
        print(f"\n--- PRINTED OCR: {file_path} ---")

        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(
                file_path,
                dpi=Config.DPI
                # poppler_path=Config.POPPLER_PATH
            )
        else:
            images = [Image.open(file_path)]

        full_text = ""

        for i, img in enumerate(images):
            processed = self.preprocess(img)

            text = pytesseract.image_to_string(
                processed,
                config='--psm 6'
            )

            full_text += text + "\n"

        return full_text.strip()


# ==================== MAIN ====================
def main():
    if not os.path.exists(Config.HANDWRITTEN_DOC):
        print("Handwritten file not found!")
        return

    if not os.path.exists(Config.PRINTED_DOC):
        print("Printed file not found!")
        return

    handwritten = HandwrittenOCR()
    printed = PrintedOCR()

    text1 = handwritten.extract_text(Config.HANDWRITTEN_DOC)
    text2 = printed.extract_text(Config.PRINTED_DOC)

    with open(Config.OUTPUT_HANDWRITTEN, "w", encoding="utf-8") as f:
        f.write(text1)

    with open(Config.OUTPUT_PRINTED, "w", encoding="utf-8") as f:
        f.write(text2)

    print("\n=== RESULTS ===")
    print("\nHandwritten:\n", text1[:500])
    print("\nPrinted:\n", text2[:500])


if __name__ == "__main__":
    main()