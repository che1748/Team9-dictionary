
from flask import Flask, render_template, request, flash, session, redirect
from DictionaryReader import DictionaryReader # Assuming dictionary_reader.py is in the same directory
from users import Users  # Make sure Users.py exists and defines the Users class
import os
from dotenv import load_dotenv
import sqlite3
from streakTracker import StreakTracker
from db import initialize_db, get_connection
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
    results = None
    search_word = request.args.get('word', '').strip().lower() # Get word from URL query string
    selected_lang = request.args.get('language', 'en') # Get language from URL query string, default to 'en'
    lang_name = "Unknown"
    current_streak  = None
    longest_streak = None
    if search_word: # Only perform search if a word is provided

        
        for lang in SUPPORTED_LANGUAGES:
            if lang["code"] == selected_lang:
                lang_name = lang["name"]
            
        try:
            # Instantiate DictionaryReader and get data
            reader = DictionaryReader(search_word, selected_lang)
            raw_results = reader.get_entry()
            if raw_results:
                results = []
                for entry in raw_results:
                    if isinstance(entry, dict): # Keep this safety check for the main entry
                        headword_data = entry.get("headword") # Get headword, no default here yet

                        word_text = "N/A"
                        pos_text = "N/A"

                        if headword_data: # Check if headword_data exists at all
                            if isinstance(headword_data, dict):
                                # Case 1: headword is a dictionary 
                                word_text = headword_data.get("text", "N/A")
                                pos_text = headword_data.get("pos", "N/A")
                            elif isinstance(headword_data, list) and len(headword_data) > 0:
                                # Case 2: headword is a list of dictionaries 
                                first_headword = headword_data[0]
                                if isinstance(first_headword, dict): # Ensure the first item is a dict
                                    word_text = first_headword.get("text", "N/A")
                                    pos_text = first_headword.get("pos", "N/A")
                                else:
                                    print(f"Warning: First headword item is not a dictionary: {first_headword}")
                            else:
                                print(f"Warning: Unexpected headword type or empty list: {headword_data} (Type: {type(headword_data)})")

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
                        print(f"Warning: Skipping unexpected item in API results: {entry} (Type: {type(entry)})")
                        flash(f"Warning: Received unexpected data from API for '{search_word}'. Some results might be missing.", 'warning')
                flash(f'Found results for "{search_word}" in {lang_name}.', 'success')
            else:
                flash(f'No results found for "{search_word}" in {lang_name}.', 'info')

        except ValueError as e:
            flash(f'Configuration Error: {e}. Please check your .env file.', 'danger')
        except Exception as e:
            flash(f'An API error occurred: {e}', 'danger')

    return render_template('index.html',
                       languages=SUPPORTED_LANGUAGES,
                       search_word=search_word,
                       selected_lang=selected_lang,
                       results=results,
                       lang_name=lang_name,
                       current_streak=current_streak,
                       longest_streak=longest_streak)


@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    user = Users(username, password)
    user.add_user()
    user.close()

    flash("✅ Registration successful! You can now log in.", "success")
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(f"🧪 Login attempt by: {username}")

    user = Users(username, password)
    if user.verify_login():
        session['username'] = username
        print(f"✅ Session set for {username}")
        flash("✅ Login successful!", "success")

        # Update streaks
        streak = StreakTracker(username)
        streak.update_streak()
        streak.close()

        user.close()
        return redirect('/dashboard')
    else:
        flash("❌ Invalid username or password.", "danger")
        print("❌ Login failed")
        user.close()
        return redirect('/')



@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page for a logged-in user.

    This function checks if a user is logged in by verifying the session.
    If the user is logged in, it retrieves the user's current and longest streak
    from the database and renders the dashboard page with this information.

    Returns:
        A redirect to the home page if the user is not logged in.
        Otherwise, renders the 'dashboard.html' template with the username,
        current streak, and longest streak.
    """
    if 'username' not in session:
        return redirect('/')

    username = session['username']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_streak, longest_streak FROM users WHERE username = ?", (username,))
    streak_data = cursor.fetchone()
    conn.close()

    return render_template('dashboard.html', username=username,
                           current_streak=streak_data[0], longest_streak=streak_data[1])

@app.route('/logout')
def logout():
    session.clear()  # or session.pop('username') if you want to keep other session keys
    flash("🚪 You have been logged out.", "info")
    return redirect('/')



@app.route('/notes')
def show_notes():
    
    conn = sqlite3.connect('dic_note.db')
    cursor = conn.cursor()
    cursor.execute("SELECT word, notes, time created_at FROM note ORDER BY time")
    notes = cursor.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)










if __name__ == '__main__':
    app.run(debug=True)