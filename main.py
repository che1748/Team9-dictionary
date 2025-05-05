import os
import DictionaryReader 
import requests
import json



if __name__ in "__main__":
    
    word = "1"
  
    

    while word != "0":
          word = input("Enter your word: ").strip().lower()
          if word == "0":
               os.system("cls")
               print("Exiting...")
          

          else:
               dictionary = DictionaryReader(word)
               data = dictionary.data_reader()
               print("Word:", data[0]['word'])
               print("Definition:", data[0]['meanings'][0]['definitions'][0]['definition'])
               os.system("pause")
               os.system("cls")
     
        

    # Assuming you have a class DictionaryReader with a method get_data that fetches data from an API
    # dictionary_reader = DictionaryReader()
    # data = dictionary_reader.get_data(word)