import os
import DictionaryReader  # Import DictionaryReader from its module
import requests
import json

def get_word_data(word):
     url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
     response = requests.get(url) 
     if response.status_code != 200:
            print("Error: Unable to fetch data")
            return None
     return response.json()

if __name__ in "__main__":
    
    word = "1"

    while word != "0":
          word = input("Enter your word: ")
          if word == "0":
               os.system("cls")
               print("Exiting...")
          else:

               data = get_word_data(word)
               print("Word:", data[0]['word'])
               print("Definition:", data[0]['meanings'][0]['definitions'][0]['definition'])
               os.system("pause")
               os.system("cls")
     
        

    # Assuming you have a class DictionaryReader with a method get_data that fetches data from an API
    # dictionary_reader = DictionaryReader()
    # data = dictionary_reader.get_data(word)