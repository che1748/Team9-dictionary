import sqlite3
import os

DB_PATH = 'user_file.db'
LOOKUP_PATH = 'lookup_history.db'

def get_user_connection(username):
    """Returns a connection to the user database."""
    return sqlite3.connect(DB_PATH)

def get_lookup_connection():
    """Returns a connection to the lookup history database."""
    return sqlite3.connect(LOOKUP_PATH)

def initialize_db():
    """Initializes both databases with required tables."""

    # Initialize users table
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

    # Initialize lookup_history table
    lookup_conn = get_lookup_connection()
    lookup_cursor = lookup_conn.cursor()

    lookup_cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            word TEXT NOT NULL,
            language_code TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    lookup_conn.commit()
    lookup_conn.close()

    print("✅ Databases initialized successfully.")
