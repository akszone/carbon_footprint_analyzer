import openai
import os
import json
import re
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_flight_info_with_ai(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts flight booking details from unstructured boarding pass text."},
                {"role": "user", "content": f"""Extract the following fields from this boarding pass text:
- flight_number
- from (as IATA airport code)
- to (as IATA airport code)
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

        # Clean triple backticks wrapper if present
        cleaned_content = re.sub(r"^```json\s*", "", content)
        cleaned_content = re.sub(r"```$", "", cleaned_content).strip()

        flight_info = json.loads(cleaned_content)
        return flight_info

    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON from AI response.")
        print("Response content:", content)
        return {}

    except Exception as e:
        print(f"❌ Error extracting data: {e}")
        return {}

