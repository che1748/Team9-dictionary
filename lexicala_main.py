# from lexicala_api import LexicalaAPI
# from utils import clear_screen
# import requests


# def choose_language():
#     languages = {
#         "1": ("English", "en"),
#         "2": ("Spanish", "es"),
#         "3": ("French", "fr"),
#         "4": ("Japanese", "ja")
#     }

#     print("\n🌍 Choose a language:")
#     for key, (name, _) in languages.items():
#         print(f"{key}. {name}")

#     choice = input("Your choice: ")
#     return languages.get(choice, ("English", "en"))[1]

# def main():
#     client = LexicalaAPI()
#     lang = "en"

#     while True:
#         print("\n📚 Dictionary Menu")
#         print("1. Choose Language")
#         print("2. Search Word")
#         print("3. Quit")

#         option = input("Select an option: ")

#         if option == "1":
#             clear_screen()
#             lang = choose_language()
            

#         elif option == "2":
#             clear_screen()
#             word = input("Enter a word: ")
#             word_search = LexicalaAPI.search_word(word, lang)
#             print(word_search)
#             # entry_id = client.search_word(word, lang)

#             # if entry_id:
#             #     entry = client.get_entry(entry_id, lang)
#             #     if entry:
#             #         headword = entry[0]["headword"]["text"]
#             #         print(f"\n🔍 Word: {headword}")
#             #         for i, sense in enumerate(entry[0]["senses"][:3], 1):
#             #             print(f"{i}. {sense['definition']['text']}")
#             #     else:
#             #         print("❌ No detailed entry found.")
#             # else:
#                 # print("❌ Word not found.")

#         elif option == "3":
#             print("👋 Goodbye!")
#             break

#         else:
#             print("❌ Invalid option.")
        
#         input("\nPress Enter to return to menu...")
#         clear_screen()

# if __name__ == "__main__":
#     main()
from lexicala_api import LexicalaAPI
from utils import clear_screen
import requests

def choose_language():
    languages = {
        "1": ("English", "en"),
        "2": ("Spanish", "es"),
        "3": ("French", "fr"),
        "4": ("Japanese", "ja")
    }

    print("\n🌍 Choose a language:")
    for key, (name, _) in languages.items():
        print(f"{key}. {name}")

    choice = input("Your choice: ")
    return languages.get(choice, ("English", "en"))[1]

def main():
    try:
        client = LexicalaAPI()  # Ensure this is properly initialized (e.g., with API key if needed)
    except Exception as e:
        print(f"❌ Failed to initialize LexicalaAPI: {e}")
        return

    lang = "en"

    while True:
        print("\n📚 Dictionary Menu")
        print("1. Choose Language")
        print("2. Search Word")
        print("3. Quit")

        option = input("Select an option: ")

        if option == "1":
            clear_screen()
            lang = choose_language()

        elif option == "2":
            clear_screen()
            word = input("Enter a word: ")
            try:
                entry_id = client.search_word(word, lang)  # Call search_word on client instance
                if entry_id:
                    entry = client.get_entry(entry_id, lang)
                    if entry:
                        headword = entry[0]["headword"]["text"]
                        print(f"\n🔍 Word: {headword}")
                        for i, sense in enumerate(entry[0]["senses"][:3], 1):
                            print(f"{i}. {sense['definition']['text']}")
                    else:
                        print("❌ No detailed entry found.")
                else:
                    print("❌ Word not found.")
            except Exception as e:
                print(f"❌ Error searching word: {e}")

        elif option == "3":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option.")

        input("\nPress Enter to return to menu...")
        clear_screen()

if __name__ == "__main__":
    main()
