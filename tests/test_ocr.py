# test_ocr.py
from utils.ocr import extract_text_from_pdf

pdf_path = "data/boarding_passes/HYD-PNQ-30Apr24.pdf"
text = extract_text_from_pdf(pdf_path)

print("Extracted Text:\n")
print(text)
