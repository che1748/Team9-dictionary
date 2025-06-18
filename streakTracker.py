from db import get_user_connection

from datetime import date, timedelta

class StreakTracker:
    def __init__(self, username):
        self.username = username
        self.conn = get_user_connection()
        self.cursor = self.conn.cursor()

    def update_streak(self):
        self.cursor.execute(
            "SELECT current_streak, longest_streak, last_active FROM users WHERE username = ?",
            (self.username,)
        )
        row = self.cursor.fetchone()

        if not row:
            print("❌ User not found.")
            return

        current_streak, longest_streak, last_active = row
        today = date.today()

        if last_active:
            last_date = date.fromisoformat(last_active)
        else:
            last_date = None

        print(f"👤 {self.username} - Last Active: {last_date}, Today: {today}")

        if last_date == today:
            print("ℹ️ Already logged in today. No change.")
            return
        elif last_date == today - timedelta(days=1):
            current_streak += 1
            print("🔥 Streak continued!")
        else:
            current_streak = 1
            print("🔄 Streak reset to 1")

        if current_streak > longest_streak:
            longest_streak = current_streak

        self.cursor.execute("""
            UPDATE users
            SET current_streak = ?, longest_streak = ?, last_active = ?
            WHERE username = ?
        """, (current_streak, longest_streak, today.isoformat(), self.username))
        self.conn.commit()

        print(f"✅ Updated: current_streak={current_streak}, longest_streak={longest_streak}, last_active={today}")

    def close(self):
        self.conn.close()
