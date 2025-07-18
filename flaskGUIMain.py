from flask import Flask, render_template, request, flash, session, redirect, url_for
from DictionaryReader import DictionaryReader # Assuming dictionary_reader.py is in the same directory
from users import Users  
import os
from dotenv import load_dotenv
import sqlite3
from streakTracker import StreakTracker
from db import initialize_db, get_user_connection
from lookup_history import LookupHistory
from language_pairs import LanguagePairs
from note import Note

load_dotenv()

app = Flask(__name__)
# It's crucial to set a secret key for Flask.
# Use a strong, random key in production.
initialize_db()
app.secret_key = os.getenv("FLASK_SECRET_KEY", "a_default_secret_key_if_not_set_in_env")

# This list matches the options in your HTML's <select> element.
# It's good practice to define it in Python too for consistency and validation.
SUPPORTED_LANGUAGES = [
    {"code": "default", "name": "Select a Language"},
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

@app.route('/', methods=['GET', 'POST'])
def index():
    username = session.get('username')

    current_streak = None
    longest_streak = None
    recent_lookups = []
    delete_history = None
    lang_stats = []
    results = []
    translated_word = None
    if request.method == 'POST':
        search_word = request.form.get('word', '').strip().lower()
        selected_lang = request.form.get('language', 'default')
        target_lang = request.form.get('target_lang', 'default')
    else:
        search_word = request.args.get('word', '').strip().lower()
        selected_lang = request.args.get('source_lang', 'default')
        target_lang = request.args.get('target_lang', 'default')

    selected_target_lang = target_lang
    source_lang = selected_lang

    def get_lang_name(code):
        return next((lang['name'] for lang in SUPPORTED_LANGUAGES if lang['code'] == code), code)

    lang_name = get_lang_name(selected_lang)

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
                            (word, get_lang_name(source), get_lang_name(target), timestamp)
                            for word, source, target, timestamp in recent_raw
                            ]
        history.close()

        lang_pair_obj = LanguagePairs()
        raw_stats = lang_pair_obj.get_top_pairs(username)
        lang_pair_obj.close()

        lang_stats = [
               (get_lang_name(src), get_lang_name(tgt), count)
               for src, tgt, count in raw_stats
           ]

        


    if search_word:
        lang_name = get_lang_name(selected_lang)
           

        try:
            reader = DictionaryReader(search_word, selected_lang)

            translated_word = reader.get_translation(target_lang, source_lang=selected_lang)

            results = reader.get_definitions(target_lang=target_lang)

            if results:
             
                    
                flash(f'Found results for "{search_word.upper()}" in {lang_name}.', 'success')
            else:
                flash(f'No results found for "{search_word.upper()}" in {lang_name}.', 'info')

            if username:
                    with LanguagePairs() as lang_pairs:
                        lang_pairs.increment_language_pair_usage(username, source_lang, target_lang)

        except ValueError as e:
            flash(f'Configuration Error: {e}. Please check your .env file.', 'danger')
        except Exception as e:
            flash(f'An API error occurred: {e}', 'danger')

    return render_template('index.html',
                           username=username,
                           current_streak=current_streak,
                           longest_streak=longest_streak,
                           languages=SUPPORTED_LANGUAGES,
                           selected_target_lang=selected_target_lang,
                           search_word=search_word,
                           selected_lang=selected_lang,
                           results=results,
                           lang_name=lang_name,
                           recent_lookups=recent_lookups,
                           delete_history=delete_history,
                           source_lang=source_lang,
                           lang_stats=lang_stats,
                           translated_word=translated_word)




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

        return redirect(url_for('index'))
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
    return redirect(url_for('index'))


@app.route('/notes', methods=['GET', 'POST'])
def show_notes():
    username = session.get('username')
    if not username:
        flash("⚠️ You need to log in to view notes.", "warning")
        return redirect(url_for('index'))

    note_obj = Note(username)
    if request.method == 'POST':
        note_content = request.form.get('note', '').strip()
        
        if note_content:
            note_obj.take_notes(note_content)
            flash("✅ Note saved.", "success")
        else:
            flash("⚠️ Note cannot be empty.", "warning")

    notes = note_obj.get_notes()
    note_obj.close()
    return render_template('notes.html', username=username, notes=notes)

@app.route('/lookup', methods=['POST'])
def lookup():
    word = request.form.get('word', '').strip()
    source_lang = request.form.get('source_lang', 'default')
    target_lang = request.form.get('target_lang', 'default')

    if not word:
        flash("⚠️ Please enter a word to look up.", "warning")
        return redirect(url_for('index'))

    if source_lang == 'default' or target_lang == 'default':
        flash("⚠️ Please select both source and target languages.", "warning")
        return redirect(url_for('index'))

    # Verify the word exists before logging
    try:
        reader = DictionaryReader(word, source_lang)
        results = reader.get_definitions(target_lang=target_lang)
        
        if results:
            # Only log if the word exists and has results
            username = session.get('username')
            if username:
                history = LookupHistory(username)
                history.log_search(word, source_lang, target_lang)
                history.close()
                
                with LanguagePairs() as lang_pairs:
                    lang_pairs.increment_language_pair_usage(username, source_lang, target_lang)
        
    except Exception as e:
        # Handle API errors but don't log failed lookups
        pass

    # Pass the query back to the index to render a result
    return redirect(url_for('index', word=word, source_lang=source_lang, target_lang=target_lang))






if __name__ == '__main__':
    app.run(debug=True)