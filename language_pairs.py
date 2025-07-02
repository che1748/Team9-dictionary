import sqlite3
from db import get_language_connection


class LanguagePairs:
    def __init__(self):
        self.conn = get_language_connection()
        self.cursor = self.conn.cursor()
        self.initialize_table()

    def initialize_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS language_pairs (
                username TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                PRIMARY KEY (username, source_lang, target_lang)
            )
        ''')
        self.conn.commit()

    def increment_language_pair_usage(self, username, source_lang, target_lang):
        self.cursor.execute('''
            INSERT INTO language_pairs (username, source_lang, target_lang, usage_count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(username, source_lang, target_lang)
            DO UPDATE SET usage_count = usage_count + 1
        ''', (username, source_lang, target_lang))
        self.conn.commit()

    def get_top_pairs(self, username, limit=5):
        self.cursor.execute('''
            SELECT source_lang, target_lang, usage_count
            FROM language_pairs
            WHERE username = ?
            ORDER BY usage_count DESC
            LIMIT ?
        ''', (username, limit))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        print("🛑 Language pairs database connection closed.")