# db.py

import sqlite3
import os

DB_PATH = 'user_file.db'  # ✅ Ensure this is the same path used across your app

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def initialize_db():
    """Initializes the database with the required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
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

    # 

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")
