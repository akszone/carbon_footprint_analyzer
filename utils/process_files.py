import os
from utils.ocr import extract_text_from_pdf
from utils.parser_ai import extract_flight_info_with_ai
from utils.emission_api import get_flight_emissions
from utils.storage import init_db, save_emission_record

def process_files_in_folder(folder_path):
    print(f"Starting to process folder on line: {folder_path}")  # <--- Add this line
    
    """
    Process all PDF files in the folder:
    - OCR to extract text
    - AI to extract flight info
    - API to calculate CO₂
    - Save results to DB
    """
   # print(f"Starting to process folder: {folder_path}")  # <--- Add this line
    init_db()
    

    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"\n📄 Processing file: {filename}")

            # Step 1: OCR
            extracted_text = extract_text_from_pdf(file_path)
           # print(f"⚠️  No text found in {extracted_text}")
            if not extracted_text:
                print(f"⚠️  No text found in {filename}")
                continue

            # Step 2: Parse flight info
            flight_info = extract_flight_info_with_ai(extracted_text)
            print(f"⚠️  No text found in {flight_info}")
            if not flight_info:
                print(f"❌ Could not extract flight info from {flight_info}")
                continue

            # Step 3: CO₂ estimate
            
            emission_data = get_flight_emissions(flight_info)
            if emission_data and "co2e" in emission_data:
                print(f"✅ CO₂ estimated: {emission_data['co2e']} {emission_data['co2e_unit']} for {filename}")
            else:
                print(f"❌ CO₂ estimation failed for {filename}")


            # Step 4: Save
            co2_kg = emission_data["co2e"]
            save_emission_record(flight_info, co2_kg)
            print(f"✅ Saved: {co2_kg:.2f} kg CO₂ for {filename}")
