import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DictionaryReader:
    def __init__(self, word, lang):
        self.word = word
        self.lang = lang
        self.api_key = os.getenv("LEXICALA_API_KEY")
        self.base_url = "https://lexicala1.p.rapidapi.com/search"
        if not self.api_key:
            raise ValueError("API key is not set.")
        self.headers = {
            "x-rapidapi-host": "lexicala1.p.rapidapi.com",
            "x-rapidapi-key": self.api_key  # Your API key
        }
        self.data = self.get_word_data()
        
        

    def get_word_data(self):
        querystring = {
            "text": self.word,  # Word to search for
            "language": self.lang,  # Language code (e.g., 'en', 'fr', 'ja')
        }
        
        try:
            # Send GET request with query parameters and headers
            response = requests.get(self.base_url, headers=self.headers, params=querystring)
            response.raise_for_status()  # Check for successful response
            
            # Check if response is successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                api_response = json.dumps(data, indent=4)  # Pretty print the JSON response
                print(f"API Response: {api_response}")
                return data.get("results", [])  # Adjust this based on the actual API response structure
            else:
                print(f"Request failed: {response.status_code}, {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def data_reader(self):
        if not self.data:
            print("No data found for the word.")
            return

        for entry in self.data:
            word = entry.get("headword", {}).get("text", "Unknown")
            pos = entry.get("headword", {}).get("pos", "Unknown")
            
            print(f"\n🔤 Word: {word}")
            print(f"📚 Part of Speech: {pos}")

            senses = entry.get("senses", [])
            if not senses:
                print("No definitions found.")
            else:
                for i, sense in enumerate(senses[:3], 1):
                    definition = sense.get("definition", "No definition found")
                    print(f"{i}. {definition}")
                    


    def get_entry(self):
        return self.data
