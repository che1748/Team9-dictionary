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
            "x-rapidapi-key": self.api_key
        }
        self.data = self.get_word_data()

    def get_word_data(self):
        querystring = {
            "text": self.word,
            "language": self.lang,
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=querystring)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                print(f"API Response: {json.dumps(data, indent=4)}")
                return data.get("results", [])
            else:
                print(f"Request failed: {response.status_code}, {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def get_entry(self): 
        return self.data

    def data_reader(self):
        data = self.get_entry()

        if not data:
            print("No data found for the word.")
            return

        for entry in data:


            # Normalize headwords to always be a list
            raw_headwords = entry.get("headword", [])
            headwords = raw_headwords if isinstance(raw_headwords, list) else [raw_headwords]

            grouped = {}
            for hw in headwords:
                word_text = hw.get("text", "")
                word_pos = hw.get("pos", "")

                if word_pos not in grouped:
                    grouped[word_pos] = []
                grouped[word_pos].append(word_text)
            #if the words are not grouped
            for pos, words in grouped.items():
                word_list = ", ".join(words)
                print(f"\n🔤 Word(s): {word_list}")
                print(f"📚 Part of Speech: {pos}\n")
            #print out the definitions
            senses = entry.get("senses", [])
            if not senses:
                print("No definitions found.")
            else:
                for i, sense in enumerate(senses, 1):
                    definition = sense.get("definition")
                    if definition:
                        print(f"{i}. {definition}\n")
