import sqlite3
from datetime import datetime


class Note:
    def __init__(self, username):
        self.username = username
        self.conn = sqlite3.connect("dic_note.db")
        self.cursor = self.conn.cursor()
        self.initialize_table()

    def initialize_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                word TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def take_notes(self, word, notes):
        '''This function takes a word and the related notes as input and stores 
        the information in a local SQLite database. The table stores the username, word, note, and the time.
        '''
        
        # Get the current time in a formatted string
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add notes into the database using the initialized connection and cursor
        self.cursor.execute(
            "INSERT INTO note (username, word, notes, created_at) VALUES (?, ?, ?, ?)",
            (self.username, word, notes, current_time)
        )
        self.conn.commit()

    def get_notes(self):
        self.cursor.execute("SELECT word, notes, created_at FROM note WHERE username = ? ORDER BY created_at", (self.username,))
        notes = self.cursor.fetchall()
        return notes

    def delete_note(self, word):
        self.cursor.execute("DELETE FROM note WHERE username = ? AND word = ?", (self.username, word))
        self.conn.commit()

    def delete_all_notes(self):
        self.cursor.execute("DELETE FROM note WHERE username = ?", (self.username,))
        self.conn.commit()
        print("All notes deleted successfully")

    def close(self):
        self.conn.close()
        print("Connection to note database closed")
