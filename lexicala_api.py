import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LexicalaAPI:
    def __init__(self):
        self.api_key = os.getenv("LEXICALA_API_KEY")
        if not self.api_key:
            raise ValueError("API key missing. Check your .env file.")
        self.base_url = "https://api.lexicala.com"

    def search_word(self, word, lang="en"):
        url = f"{self.base_url}/search?text={word}&language={lang}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json().get("results", [])
            return results[0]["id"] if results else None
        else:
            print("❌ API error:", response.status_code)
            return None

    def get_entry(self, entry_id, lang="en"):
        url = f"{self.base_url}/entries/{entry_id}?language={lang}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Entry fetch error:", response.status_code)
            return None
