import openai
import os

from dotenv import load_dotenv
load_dotenv()

# Set your API key (better to load from env in production)
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_flight_info_with_ai(text):
    """
    Use OpenAI Chat API to extract structured flight info from boarding pass text.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            #model="gpt-4",  # or "gpt-3.5-turbo" for lower cost
            messages=[
                {"role": "system", "content": "You are an assistant that extracts flight booking details from unstructured boarding pass text."},
                {"role": "user", "content": f"""Extract the following fields from this boarding pass text:
- flight_number
- from
- to
- date
- class
- airline

Return only a JSON object with those keys.

Text:
{text}
"""}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None
    



    ++++++++++++++++++++++++++++Emmision FileExistsError
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
        print("Missing origin or destination.")
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
                "class": flight_class
            }
        ]
    }

    response = requests.post("https://api.climatiq.io/travel/flights", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print("Emission API error:", response.status_code, response.text)
        return None

