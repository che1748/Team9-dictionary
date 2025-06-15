
from db import get_connection
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def add_user(self):
        try:
            hashed_pw = generate_password_hash(self.password)
            self.cursor.execute(
                "INSERT INTO users (username, password, last_active) VALUES (?, ?, ?)",
                (self.username, hashed_pw, date.today().isoformat())
            )
            self.conn.commit()
            print(f"✅ User '{self.username}' added to database.")
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


    def close(self):
        self.conn.close()
