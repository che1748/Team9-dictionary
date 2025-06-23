import sqlite3
from datetime import datetime
from db import get_lookup_connection

class LookupHistory:  
    def __init__(self, username):
        self.username = username
        self.conn = get_lookup_connection()
        self.cursor = self.conn.cursor()

    def log_search(self, word, language_code):  
        self.cursor.execute(
            "INSERT INTO lookup_history (username, word, language_code, timestamp) VALUES (?, ?, ?, ?)",
            (self.username, word, language_code, datetime.now())
        )
        self.conn.commit()
        print(f"✅ Word '{word}' looked up in '{language_code}' successfully.")

    def get_recent_history(self, limit=10):
        self.cursor.execute(
            "SELECT word, language_code, timestamp FROM lookup_history WHERE username = ? ORDER BY timestamp DESC LIMIT ?",
            (self.username, limit)
        )
        return self.cursor.fetchall()

    def clear_all_history(self):
        self.cursor.execute(
            "DELETE FROM lookup_history WHERE username = ?",
            (self.username,)
        )
        self.conn.commit()
        print(f"🗑️ All history cleared for user '{self.username}'.")


    def close(self):
        self.conn.close()
        print("🛑 Database connection closed.")
