import os
from DictionaryReader import DictionaryReader 
from lexicala_api import LexicalaAPI 
import lexicala_main

def main():
    word = "1"
    supported_languages = ['en', 'fr', 'ja', 'es']

    while word != "0":
        word = input("Enter your word (or 0 to exit): ").strip().lower()
        if word == "0":
            os.system("cls")
            print("Exiting...")
            return 

        language = input("Enter the language (e.g., 'en' for English): ").strip().lower()
        while language not in supported_languages:
            print("Language not supported. Choose from: en, fr, ja, es")
            language = input("Enter the language again: ").strip().lower()
        
        os.system("cls")
        print("Fetching data...")

        dictionary_reader = DictionaryReader(word, language)
        data = dictionary_reader.get_entry()

        if not data:
            print("No data found for the word.")
        else:
            dictionary_reader.data_reader()

        input("\nPress Enter to continue...")
        os.system("cls")

if __name__ == "__main__":  
    main()

        
 
    # Assuming you have a class DictionaryReader with a method get_data that fetches data from an API
    # dictionary_reader = DictionaryReader()
    # data = dictionary_reader.get_data(word)




import requests

# Put your API key here
# api_key = "57e1cbd235msh7af6ea007827d41p10aa13jsn7772d6aab5ef"

# # Example search: the word "casa" in Spanish
# url = "https://lexicala1.p.rapidapi.com/search"
# querystring = {
#     "text": "house",
#     "language": "en"  # 'en' for English, 'fr' for French, 'ja' for Japanese, etc.
# }

# headers = {
#     "x-rapidapi-host": "lexicala1.p.rapidapi.com",
#     "x-rapidapi-key": api_key
# }

# response = requests.get(url, headers=headers, params=querystring)

# # Print raw JSON
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print("Request failed:", response.status_code, response.text)
