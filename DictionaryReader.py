import requests
import json

class DictionaryReader:
  
    def get_data(self, word):
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/word"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()