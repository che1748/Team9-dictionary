import requests
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

def normalize_for_translator(lang_code):
    """Normalize language codes for compatibility with GoogleTranslator."""
    if lang_code == "br":
        return "pt"
    return lang_code

class DictionaryReader:
    def __init__(self, word, lang='en'):
        self.word = word
        self.lang = lang
        self.api_key = os.getenv("LEXICALA_API_KEY")
        self.base_url = "https://lexicala1.p.rapidapi.com/search"

        if not self.api_key:
            raise ValueError("API key is not set.")

        self.headers = {
            "x-rapidapi-host": "lexicala1.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }

        self.data = self.get_word_data()

    def get_translation(self, target_lang, source_lang='auto'):
        try:
            source_norm = normalize_for_translator(source_lang)
            target_norm = normalize_for_translator(target_lang)
            return GoogleTranslator(source=source_norm, target=target_norm).translate(self.word)
        except Exception as e:
            print(f"Translation error from '{source_lang}' to '{target_lang}': {e}")
            return "Translation failed."

    def get_word_data(self):
        querystring = {
            "text": self.word,
            "language": self.lang
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=querystring)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
        return None

    def get_definitions(self, target_lang=None):
        entries = self.get_entry()
        results = []

        if not entries:
            return results

        for entry in entries:
            raw_headwords = entry.get("headword", [])
            headwords = raw_headwords if isinstance(raw_headwords, list) else [raw_headwords]

            grouped = {}
            for hw in headwords:
                word_text = hw.get("text", "")
                word_pos = hw.get("pos", "")
                if word_pos not in grouped:
                    grouped[word_pos] = []
                grouped[word_pos].append(word_text)

            senses = entry.get("senses", [])
            sense_defs = []
            for i, sense in enumerate(senses[:3], 1):
                definition = sense.get("definition")
                translated_def = None

                if definition:
                    if target_lang and target_lang != self.lang:
                        try:
                            translated_def = GoogleTranslator(
                                source=normalize_for_translator(self.lang),
                                target=normalize_for_translator(target_lang)
                            ).translate(definition)
                        except Exception as e:
                            print(f"Definition translation error: {e}")
                            translated_def = "Translation failed."
                    else:
                        translated_def = definition

                    sense_defs.append({
                        "original": f"{i}. {definition}",
                        "translated": f"{i}. {translated_def}" if translated_def else None
                    })

            for pos, words in grouped.items():
                if target_lang and target_lang != self.lang:
                    try:
                        translated_pos = GoogleTranslator(
                            source='en',
                            target=normalize_for_translator(target_lang)
                        ).translate(pos)
                    except Exception as e:
                        print(f"POS translation error: {e}")
                        translated_pos = pos

                    try:
                        translated_words = [
                            GoogleTranslator(
                                source=normalize_for_translator(self.lang),
                                target=normalize_for_translator(target_lang)
                            ).translate(w) for w in words
                        ]
                    except Exception as e:
                        print(f"Headword translation error: {e}")
                        translated_words = words
                else:
                    translated_pos = pos
                    translated_words = words

                results.append({
                    "word": ", ".join(words),
                    "translated_word": ", ".join(translated_words),
                    "pos": pos,
                    "translated_pos": translated_pos,
                    "definitions": sense_defs or [{"original": "No definitions found.", "translated": None}]
                })

        return results

    def get_entry(self):
        return self.data
