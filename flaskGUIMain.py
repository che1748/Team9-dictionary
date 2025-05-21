# app.py
from flask import Flask, render_template, request, flash
from DictionaryReader import DictionaryReader # Assuming dictionary_reader.py is in the same directory
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# It's crucial to set a secret key for Flask.
# Use a strong, random key in production.
app.secret_key = os.getenv("FLASK_SECRET_KEY", "a_default_secret_key_if_not_set_in_env")

# This list matches the options in your HTML's <select> element.
# It's good practice to define it in Python too for consistency and validation.
SUPPORTED_LANGUAGES = [
    {"code": "ar", "name": "Arabic"},
    {"code": "ca", "name": "Catalan"},
    {"code": "zh", "name": "Chinese (Simplified)"},
    {"code": "tw", "name": "Chinese (Traditional / Taiwan)"},
    {"code": "hr", "name": "Croatian"},
    {"code": "cs", "name": "Czech"},
    {"code": "da", "name": "Danish"},
    {"code": "nl", "name": "Dutch"},
    {"code": "en", "name": "English"},
    {"code": "et", "name": "Estonian"},
    {"code": "fi", "name": "Finnish"},
    {"code": "fr", "name": "French"},
    {"code": "fy", "name": "Frisian"},
    {"code": "de", "name": "German"},
    {"code": "el", "name": "Greek"},
    {"code": "he", "name": "Hebrew"},
    {"code": "hi", "name": "Hindi"},
    {"code": "hu", "name": "Hungarian"},
    {"code": "id", "name": "Indonesian"},
    {"code": "it", "name": "Italian"},
    {"code": "ja", "name": "Japanese"},
    {"code": "ko", "name": "Korean"},
    {"code": "la", "name": "Latin"},
    {"code": "lv", "name": "Latvian"},
    {"code": "ml", "name": "Malayalam"},
    {"code": "no", "name": "Norwegian"},
    {"code": "pl", "name": "Polish"},
    {"code": "br", "name": "Breton"},
    {"code": "pt", "name": "Portuguese"},
    {"code": "ru", "name": "Russian"},
    {"code": "sl", "name": "Slovenian"},
    {"code": "es", "name": "Spanish"},
    {"code": "sv", "name": "Swedish"},
    {"code": "th", "name": "Thai"},
    {"code": "tr", "name": "Turkish"},
    {"code": "uk", "name": "Ukrainian"},
]

@app.route('/', methods=['GET'])
def index():
    results = None
    search_word = request.args.get('word', '').strip() # Get word from URL query string
    selected_lang = request.args.get('language', 'en') # Get language from URL query string, default to 'en'

    if search_word: # Only perform search if a word is provided
        try:
            # Instantiate DictionaryReader and get data
            reader = DictionaryReader(search_word, selected_lang)
            raw_results = reader.get_entry()

            if raw_results:
                results = []
                for entry in raw_results:
                    formatted_entry = {
                        "word": entry.get("headword", {}).get("text", "N/A"),
                        "pos": entry.get("headword", {}).get("pos", "N/A"),
                        "definitions": []
                    }
                    senses = entry.get("senses", [])
                    if senses:
                        # Limiting to top 3 definitions as in your original data_reader
                        for i, sense in enumerate(senses[:3], 1):
                            definition = sense.get("definition", "No definition found")
                            formatted_entry["definitions"].append(f"{i}. {definition}")
                    else:
                        formatted_entry["definitions"].append("No definitions found for this entry.")
                    results.append(formatted_entry)
                flash(f'Found results for "{search_word}" in {selected_lang}.', 'success')
            else:
                flash(f'No results found for "{search_word}" in {selected_lang}.', 'info')

        except ValueError as e:
            flash(f'Configuration Error: {e}. Please check your .env file.', 'danger')
        except Exception as e:
            flash(f'An API error occurred: {e}', 'danger')

    return render_template('index.html',
                           languages=SUPPORTED_LANGUAGES,
                           search_word=search_word,
                           selected_lang=selected_lang,
                           results=results)

if __name__ == '__main__':
    # Make sure to set FLASK_SECRET_KEY in your .env for flash messages to work
    # and LEXICALA_API_KEY for DictionaryReader.
    app.run(debug=True)