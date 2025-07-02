import logging
from datetime import date, timedelta
from sqlite3 import Connection, Cursor
from db import get_user_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class StreakTracker:
    def __init__(self, username: str):
        self.username: str = username
        try:
            self.conn: Connection = get_user_connection()
            self.cursor: Cursor = self.conn.cursor()
        except Exception as e:
            logging.error(f"Failed to connect to the database for user '{self.username}': {e}")
            raise

    def update_streak(self) -> None:
        try:
            self.cursor.execute("""
                SELECT current_streak, longest_streak, last_active
                FROM users
                WHERE username = ?
            """, (self.username,))
            row = self.cursor.fetchone()
        except Exception as e:
            logging.error(f"Database query error: {e}")
            return

        if not row:
            logging.error(f"User '{self.username}' not found in the database.")
            return

        current_streak, longest_streak, last_active = row
        today = date.today()

        try:
            last_date = date.fromisoformat(str(last_active)) if last_active else None
        except (ValueError, TypeError):
            logging.warning(f"Invalid last_active format for '{self.username}': {last_active}")
            last_date = None

        logging.info(f"{self.username} - Last Active: {last_date}, Today: {today}")

        if last_date == today:
            logging.info("Already active today. No streak change.")
            return
        elif last_date is not None and last_date in [today - timedelta(days=1), today - timedelta(days=2)]:
            current_streak += 1
            logging.info("Streak continued with grace day!")
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 1
            logging.info("Streak reset to 1 or first activity.")

        if current_streak > longest_streak:
            longest_streak = current_streak

        try:
            self.cursor.execute("""
                UPDATE users
                SET current_streak = ?, longest_streak = ?, last_active = ?
                WHERE username = ?
            """, (current_streak, longest_streak, today.isoformat(), self.username))
            self.conn.commit()
            logging.info(f"Streak updated: current={current_streak}, longest={longest_streak}, last_active={today}")
        except Exception as e:
            logging.error(f"Failed to update streak for '{self.username}': {e}")
            print(f"❌ Failed to update streak for '{self.username}': {e}")

    def close(self) -> None:
        try:
            self.conn.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.warning(f"Error closing the database connection: {e}")
            print(f"⚠️ Error closing the database connection: {e}")
