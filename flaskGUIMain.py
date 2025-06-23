from flask import Flask, render_template, request, flash, session, redirect, url_for
from DictionaryReader import DictionaryReader # Assuming dictionary_reader.py is in the same directory
from users import Users  # Make sure Users.py exists and defines the Users class
import os
from dotenv import load_dotenv
import sqlite3
from streakTracker import StreakTracker
from db import initialize_db, get_user_connection
from lookup_history import LookupHistory
load_dotenv()

app = Flask(__name__)
# It's crucial to set a secret key for Flask.
# Use a strong, random key in production.
initialize_db()
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
    {"code": "pt", "name": "Portuguese (Portugal)"},
    {"code": "br", "name": "Portuguese(Brazil)"},
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
    username = session.get('username')
    
    current_streak = None
    longest_streak = None
    recent_lookups = []
    delete_history = None

    if username:
        conn = get_user_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_streak, longest_streak FROM users WHERE username = ?", (username,))
        streak_data = cursor.fetchone()
        conn.close()
        if streak_data:
            current_streak, longest_streak = streak_data
        history = LookupHistory(username)
        recent_raw = history.get_recent_history(limit=10)
        recent_lookups = [
        (word, next((lang['name'] for lang in SUPPORTED_LANGUAGES if lang['code'] == code), code), timestamp)
        for word, code, timestamp in recent_raw]

        history.close()
    results = []
    search_word = request.args.get('word', '').strip().lower()
    selected_lang = request.args.get('language', 'en')
    lang_name = " "

    if search_word:
        for lang in SUPPORTED_LANGUAGES:
            if lang["code"] == selected_lang:
                lang_name = lang["name"]

        try:
            reader = DictionaryReader(search_word, selected_lang)
            raw_results = reader.get_entry()
            if raw_results:
                results = []
                for entry in raw_results:
                    if isinstance(entry, dict):
                        headword_data = entry.get("headword")
                        word_text = "N/A"
                        pos_text = "N/A"

                        if headword_data:
                            if isinstance(headword_data, dict):
                                word_text = headword_data.get("text", "N/A")
                                pos_text = headword_data.get("pos", "N/A")
                            elif isinstance(headword_data, list) and len(headword_data) > 0:
                                first_headword = headword_data[0]
                                if isinstance(first_headword, dict):
                                    word_text = first_headword.get("text", "N/A")
                                    pos_text = first_headword.get("pos", "N/A")

                        formatted_entry = {
                            "word": word_text,
                            "pos": pos_text,
                            "definitions": []
                        }

                        senses = entry.get("senses", [])
                        if senses:
                            for i, sense in enumerate(senses[:3], 1):
                                definition = sense.get("definition", "No definition found")
                                formatted_entry["definitions"].append(f"{i}. {definition}")
                        else:
                            formatted_entry["definitions"].append("No definitions found for this entry.")

                        results.append(formatted_entry)
                    else:
                        flash(f"Warning: Received unexpected data from API for '{search_word}'.", 'warning')

                flash(f'Found results for "{search_word}" in {lang_name}.', 'success')
                
                if username and search_word and raw_results:
                    history = LookupHistory(username)
                    history.log_search(search_word, selected_lang)
                    history.close()
                elif username and search_word:
                    delete_history = LookupHistory(username)
                    delete_history.clear_history(search_word, selected_lang)
                    delete_history.close()

            else:
                flash(f'No results found for "{search_word.upper()}" in {lang_name}.', 'info')
            

        except ValueError as e:
            flash(f'Configuration Error: {e}. Please check your .env file.', 'danger')
        except Exception as e:
            flash(f'An API error occurred: {e}', 'danger')

    return render_template('index.html',
                           username=username,
                           current_streak=current_streak,
                           longest_streak=longest_streak,
                           languages=SUPPORTED_LANGUAGES,
                           search_word=search_word,
                           selected_lang=selected_lang,
                           results=results,
                           lang_name=lang_name,
                           recent_lookups=recent_lookups,
                           delete_history=delete_history
                           )



@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    user = Users(username, password)
    success = user.add_user()
    user.close()

    if success:
        flash("✅ Registration successful! You can now log in.", "success")
        return redirect('/login')
    else:
        flash("❌ Registration failed. Username may already exist.", "danger")
        return redirect('/register')



@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username:
        username = username.strip()
    if password:
        password = password.strip()

    print(f"🧪 Login attempt by: {username}")

    if not username or not password:
        flash("⚠️ Username and password are required.", "warning")
        return redirect('/login')

    user = Users(username, password)

    if user.verify_login():
        session['username'] = username
        flash("✅ Login successful!", "success")
        print(f"✅ Session set for {username}")

        streak = None
        try:
            streak = StreakTracker(username)
            streak.update_streak()
        except Exception as e:
            # handle or log the error
            print(f"Error initializing streak tracker: {e}")
        finally:
            if streak is not None:
                streak.close()
            user.close()

        return redirect('/')
    else:
        flash("❌ Invalid username or password.", "danger")
        print("❌ Login failed")
        user.close()
        return redirect('/login')


@app.route('/clear')
def clear_lookup_history():
    username = session.get('username')
    if username:
        history = LookupHistory(username)
        history.clear_all_history()
        history.close()
        flash("Your lookup history has been cleared.")
    return redirect(url_for('index'))  



@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove only the username from session
    flash("🚪 You have been logged out.", "info")
    return redirect('/')



@app.route('/notes')
def show_notes():
    conn = sqlite3.connect('dic_note.db')
    cursor = conn.cursor()
    # Ensure the 'note' table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT word, notes, created_at FROM note ORDER BY created_at")
    notes = cursor.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)










if __name__ == '__main__':
    app.run(debug=True)