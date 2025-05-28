
try:
    from utils.process_files import process_files_in_folder
    from utils.reports import total_co2_emissions, flights_by_month
except Exception as e:
    print(f"Import failed: {e}")

#print("This print runs even if import fails.")


def print_report():
    total = total_co2_emissions()
    monthly = flights_by_month()

    print("\n📊 --- Emission Summary Report ---")
    print(f"Total CO₂ Emissions: {total:.2f} kg")
    print("Flights by Month:")
    for month, count in monthly.items():
        print(f"  {month}: {count} flights")

if __name__ == "__main__":
    folder_path = "data/boarding_passes"
   # print(f"Starting to process folder: {folder_path}")  # <--- Add this line
    process_files_in_folder(folder_path)
    print_report()
