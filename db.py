import sqlite3
import os

DB_PATH = 'user_file.db'
LOOKUP_PATH = 'lookup_history.db'
LANGUAGE_PAIRS = 'language_pairs.db'
NOTES = 'dic_note.db'

def get_user_connection():
    """Returns a connection to the user database."""
    return sqlite3.connect(DB_PATH)

def get_lookup_connection():
    """Returns a connection to the lookup history database."""
    return sqlite3.connect(LOOKUP_PATH)

def get_language_connection():
    """Returns a connection to the language pairs database."""
    return sqlite3.connect(LANGUAGE_PAIRS)
def get_notes_connection():
    """Returns a connection to the notes database."""
    return sqlite3.connect(NOTES)

def initialize_db():
    """Initializes all databases with required tables."""

    # === Users DB ===
    user_conn = get_user_connection()
    user_cursor = user_conn.cursor()
    user_cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_active TEXT
        )
    ''')
    user_conn.commit()
    user_conn.close()

    # === Lookup History DB ===
    lookup_conn = get_lookup_connection()
    lookup_cursor = lookup_conn.cursor()

    # Drop old version and recreate clean table
    lookup_cursor.execute('''
    CREATE TABLE IF NOT EXISTS lookup_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        word TEXT NOT NULL,
        source_lang TEXT NOT NULL,
        target_lang TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    lookup_conn.commit()
    lookup_conn.close()

    # === Language Pairs DB ===
    language_conn = get_language_connection()
    language_cursor = language_conn.cursor()
    language_cursor.execute('''
        CREATE TABLE IF NOT EXISTS language_pairs (
            username TEXT NOT NULL,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0,
            PRIMARY KEY (username, source_lang, target_lang)
        )
    ''')
    language_conn.commit()
    language_conn.close()

    # === Notes DB ===
    notes_conn = get_notes_connection()
    notes_cursor = notes_conn.cursor()
    # Ensure the 'note' table exists
    notes_cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            word TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    notes_conn.commit()
    notes_conn.close()




    print("✅ All databases initialized successfully.")
