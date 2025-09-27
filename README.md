# Multilingual Dictionary (Team9)

Live App: [https://multiligual-dictionary.onrender.com/](https://multiligual-dictionary.onrender.com/)

## Overview
This project is a full-stack multilingual dictionary web app built for CSE 310. It allows users to look up words, get definitions, and translate between 40+ languages. The app is deployed and accessible on Render.

## Features
- Lookup definitions for words in multiple languages
- Translate words and definitions between supported languages
- User authentication (register/login/logout)
- Track lookup history and most-used language pairs
- Streak tracking for daily lookups
- Personal notes for users
- Responsive, modern UI (Flask + HTML/CSS)

## Structure

**Backend:**
- `flaskGUIMain.py`: Main Flask app, routes, and logic
- `DictionaryReader.py`: Handles dictionary lookups and translation
- `users.py`, `db.py`: User management and database setup
- `lookup_history.py`, `language_pairs.py`, `streakTracker.py`, `note.py`: User features (history, stats, notes)

**Frontend:**
- `templates/`: HTML templates (Jinja2)
- `static/`: CSS and images

**Databases:**
- `user_file.db`, `lookup_history.db`, `language_pairs.db`, `dic_note.db`: SQLite databases for users, lookups, stats, and notes

## Lexicala API & Implementation
The core dictionary data is fetched from the [Lexicala API](https://rapidapi.com/lexicala/api/lexicala1/). The API is accessed in `DictionaryReader.py` using a secure API key (set in `.env`).

**How it works:**
- When a user searches for a word, the app queries Lexicala for definitions in the selected language.
- The API response is parsed for headwords, part of speech, and up to 3 definitions per entry.
- If the user requests a translation, the app uses the `deep_translator` package (GoogleTranslator) to translate both the word and its definitions to the target language.
- Language code normalization is handled for compatibility (e.g., `br` to `pt`, `zh` to `zh-CN`).

## Main Functions & Flow
- **DictionaryReader**: Handles all API requests, translation, and parsing of results.
  - `get_translation(target_lang, source_lang)`: Uses GoogleTranslator to translate the word.
  - `get_definitions(target_lang)`: Gets definitions from Lexicala and translates them if needed.
- **User Management**: Registration, login, and streaks are managed in `users.py` and `streakTracker.py`.
- **History & Stats**: Lookups and language pair usage are tracked in `lookup_history.py` and `language_pairs.py`.
- **Notes**: Users can save notes for words in `note.py`.

## Technologies Used
- Python 3, Flask, SQLite
- Lexicala API (via RapidAPI)
- deep_translator (GoogleTranslator)
- HTML, CSS (custom, responsive)

## How to Run Locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set up a `.env` file with your Lexicala API key
4. Run: `python flaskGUIMain.py`
5. Visit `http://localhost:5000`

## Credits
Team 9, CSE 310
Deployed on Render: [https://multiligual-dictionary.onrender.com/](https://multiligual-dictionary.onrender.com/)