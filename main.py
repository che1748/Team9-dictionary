import os
from DictionaryReader import DictionaryReader  
import requests
import json

def main():
         
    word = "1"
    
    while word != "0":
        word = input("Enter your word: ").strip().lower()
     #   Specify the language
     #    language = print("Enter the language (e.g., 'en' for English): ").strip().lower()
        
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
        

    # Assuming you have a class DictionaryReader with a method get_data that fetches data from an API
    # dictionary_reader = DictionaryReader()
    # data = dictionary_reader.get_data(word)