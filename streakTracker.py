from datetime import date, timedelta
from db import get_user_connection

class StreakTracker:
    def __init__(self, username):
        self.username = username
        self.conn = get_user_connection(self.username)
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
            try:
                last_date = date.fromisoformat(str(last_active))
            except (ValueError, TypeError):
                print(f"⚠️ Invalid last_active for '{self.username}': {last_active}")
                raise
        else:
            last_date = None

        print(f"👤 {self.username} - Last Active: {last_date}, Today: {today}")

        if last_date == today:
            print("ℹ️ Already logged in today. No change.")
            return
        elif last_date in [today - timedelta(days=1), today - timedelta(days=2)]:
            current_streak += 1
            print("🔥 Streak continued (grace day allowed)!")
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
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

        print(f"✅ Updated streak: current={current_streak}, longest={longest_streak}, last_active={today}")

    def close(self):
        self.conn.close()
        print("🛑 Database connection closed.")
