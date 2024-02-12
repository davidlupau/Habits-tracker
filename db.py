import sqlite3


def get_db(name="main.db"):
    """Create a database connection to the SQLite database specified by name"""
    db = sqlite3.connect(name)
    return db


def create_tables(db):
    """Create tables for errors messages, streaks, checkoffs and habits from the create_table_sql statement"""
    cursor = db.cursor()

    # Creation of the table for error messages
    cursor.execute(""" CREATE TABLE IF NOT EXISTS errors (
        error_id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_message TEXT NOT NULL); """)

    # Creation of the table to store habits
    cursor.execute("""CREATE TABLE IF NOT EXISTS habits (
        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        periodicity TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP NULL,
        is_active BOOLEAN DEFAULT 1,
        created_by TEXT DEFAULT 'user');""")

    # Creation of the table to store completion habits info
    cursor.execute("""CREATE TABLE IF NOT EXISTS checkoffs (
        checkoff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        checkedoff_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (habit_id) REFERENCES habits(habit_id));""")

    # Creation of the table to store info about streaks
    cursor.execute("""CREATE TABLE IF NOT EXISTS streaks (
        streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP,
        FOREIGN KEY(habit_id) REFERENCES habits(habit_id));""")

    db.commit()
