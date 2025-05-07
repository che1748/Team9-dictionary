import requests
import json

class DictionaryReader:

    def __init__(self, word):
        self.word = word
        self.data = self.get_word_data()  # Removed the argument 'word'
  
    def check_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None
    
    def get_word_data(self):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"
        response = requests.get(url) 
        if response.status_code != 200:
            print("Error: Unable to fetch data")
            return None
        return response.json()

    def data_reader(self, data):
        if data:
            # Print the word and its meanings
            for entry in data:
                print(f"Word: {entry['word']}")
                for meaning in entry['meanings']:
                    print(f"Part of Speech: {meaning['partOfSpeech']}")
                    for definition in meaning['definitions']:
                        print(f"Definition: {definition['definition']}")
        else:
            print("No data found for the word.")