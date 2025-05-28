import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY")

def get_flight_emissions(flight_info):
    origin = flight_info.get("from")
    destination = flight_info.get("to")
    flight_class = flight_info.get("class", "economy").lower()

    if not origin or not destination:
        print("❌ Missing origin or destination.")
        return None

    headers = {
        "Authorization": f"Bearer {CLIMATIQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "legs": [
            {
                "from": origin,
                "to": destination,
                "passengers": 1,
                "class": "economy"
            }
        ]
    }

    print("🚀 Sending request to Climatiq API with payload:")
    print(payload)

    response = requests.post("https://api.climatiq.io/travel/flights", headers=headers, json=payload)

    if response.status_code == 200:
        print("@@@@", response.json())
        return response.json()
    else:
        print("❌ Emission API error:", response.status_code)
        print("Response text:", response.text)
        return None

