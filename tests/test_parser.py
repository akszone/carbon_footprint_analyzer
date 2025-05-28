# tests/test_parser.py
import sys
import os
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# tests/test_openai_api.py
from utils.parser_ai import extract_flight_info_with_ai
from utils.ocr import extract_text_from_pdf

# Path to the boarding pass PDF
pdf_path = "data/boarding_passes/HYD-PNQ-30Apr24.pdf"
text = extract_text_from_pdf(pdf_path)

# Call the OpenAI API to extract flight information
flight_info = extract_flight_info_with_ai(text)

print("Extracted flight info using AI:")
print(flight_info)
