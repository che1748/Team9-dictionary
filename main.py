""" import os
from DictionaryReader import DictionaryReader 
from lexicala_api import LexicalaAPI 
import lexicala_main



def main():
         
    word = "1"
    
    while word != "0":
        word = input("Enter your word: ").strip().lower()
     #   Specify the language
        language = print("Enter the language (e.g., 'en' for English): ").strip().lower()
        if language == "English":
            
        
        if word == "0":
            os.system("cls")
            print("Exiting...")
        else:
            # Create an instance of DictionaryReader
            os.system("cls")
            dictionary_reader = DictionaryReader(word)
            
            # Fetch and display the word data
            data = dictionary_reader.get_word_data()
            if data:
                dictionary_reader.data_reader(data)
            else:
                print("No data found for the word.")
            
            input("Press Enter to continue...")
            os.system("cls")
               #    print("Word:", data[0]['word'])
               #    print("Definition:", data[0]['meanings'][0]['definitions'][0]['definition'])
               #    os.system("pause")
               #    os.system("cls")






if __name__ in "__main__":
     main()
        
 """
    # Assuming you have a class DictionaryReader with a method get_data that fetches data from an API
    # dictionary_reader = DictionaryReader()
    # data = dictionary_reader.get_data(word)

import requests

# Put your API key here
api_key = "57e1cbd235msh7af6ea007827d41p10aa13jsn7772d6aab5ef"

# Example search: the word "casa" in Spanish
url = "https://lexicala1.p.rapidapi.com/search"
querystring = {
    "text": "house",
    "language": "en"  # 'en' for English, 'fr' for French, 'ja' for Japanese, etc.
}

headers = {
    "x-rapidapi-host": "lexicala1.p.rapidapi.com",
    "x-rapidapi-key": api_key
}

response = requests.get(url, headers=headers, params=querystring)

# Print raw JSON
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Request failed:", response.status_code, response.text)
