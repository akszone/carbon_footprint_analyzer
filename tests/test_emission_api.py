import sys
import os
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.emission_api import get_flight_emissions

# Replace this with real output from your parser
flight_info = {
    "from": "JFK",
    "to": "LHR",
}

result = get_flight_emissions(flight_info)

print("\n📊 Estimated Emissions:")
print(result)
