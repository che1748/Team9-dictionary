import requests
import json

class DictionaryReader:

    def __init__(self, word):
        self.word = word
        self.data = self.get_word_data()  # Removed the argument 'word'
  
    def check_data(self, url): ## This function checks if the data is available or not
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None
   
   
    ## we will need parameters self, word , language = '',
    def get_word_data(self): ## This function fetches the data from the API
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"
        response = requests.get(url) 
        if response.status_code != 200:
            print("Error: Unable to fetch data")
            return None
        return response.json()

    def data_reader(self, data): ## This function reads the data and prints it in a readable format
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


    ## add get entry function to get the entry of the word
    