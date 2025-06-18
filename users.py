import sqlite3
from db import get_user_connection
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash



class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.conn = get_user_connection()
        self.cursor = self.conn.cursor()

    def add_user(self):
        try:
            hashed_pw = generate_password_hash(self.password)
            self.cursor.execute(
                "INSERT INTO users (username, password, last_active) VALUES (?, ?, ?)",
                (self.username, hashed_pw, date.today().isoformat())
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"❌ Username '{self.username}' already exists.")
        except Exception as e:
            print(f"⚠️ Could not add user '{self.username}': {e}")


    def verify_login(self):
        self.cursor.execute("SELECT password FROM users WHERE username = ?", (self.username,))
        result = self.cursor.fetchone()

        if result is None:
            print("❌ Username not found.")
            return False

        stored_password = result[0]
        if check_password_hash(stored_password, self.password):
            print("✅ Login successful.")
            return True
        else:
            print("❌ Incorrect password.")
            return False

    def update_last_active(self):
        today = date.today().isoformat()
        self.cursor.execute(
            "UPDATE users SET last_active = ? WHERE username = ?",
            (today, self.username)
        )
        self.conn.commit()
        print(f"📅 Updated last_active for {self.username} to {today}")


    def close(self):
        self.conn.close()
