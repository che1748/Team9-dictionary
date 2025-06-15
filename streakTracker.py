# streaks.py
from db import get_connection
from datetime import date, timedelta

class StreakTracker:
    def __init__(self, username):
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def update_streak(self):
        self.cursor.execute(
            "SELECT current_streak, longest_streak, last_active FROM users WHERE username = ?",
            (self.username,)
        )
        result = self.cursor.fetchone()

        if not result:
            print("❌ User not found.")
            return

        current_streak, longest_streak, last_active = result
        today = date.today()
        today_str = today.isoformat()

        if last_active == today_str:
            print("⏳ Streak already updated today.")
            return

        last_date = date.fromisoformat(last_active) if last_active else today - timedelta(days=2)

        if last_date == today - timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1

        longest_streak = max(current_streak, longest_streak)

        self.cursor.execute('''
            UPDATE users
            SET current_streak = ?, longest_streak = ?, last_active = ?
            WHERE username = ?
        ''', (current_streak, longest_streak, today_str, self.username))

        self.conn.commit()
        print(f"🔥 Streak updated: {current_streak} (Longest: {longest_streak})")

    def close(self):
        self.conn.close()
