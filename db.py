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
		created_on DATE DEFAULT (date('now')),
		updated_on DATE DEFAULT (date('now')),
		deleted_on DATE NULL,
		is_active BOOLEAN DEFAULT 1,
		created_by TEXT DEFAULT 'user');""")

	# Creation of the table to store completion habits info
	cursor.execute("""CREATE TABLE IF NOT EXISTS checkoffs (
		checkoff_id INTEGER PRIMARY KEY AUTOINCREMENT,
		habit_id INTEGER,
		checkedoff_on DATE DEFAULT (date('now')),
		FOREIGN KEY (habit_id) REFERENCES habits(habit_id));""")

	# Creation of the table to store info about streaks
	cursor.execute("""CREATE TABLE IF NOT EXISTS streaks (
		streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
		habit_id INTEGER,
		started_on DATE DEFAULT (date('now')),
		ended_on DATE,
		FOREIGN KEY(habit_id) REFERENCES habits(habit_id));""")

	db.commit()

# Functions to interact with errors table
"""Function to add error messages to the errors table"""
def add_errors(db, error_message):
	cur = db.cursor()
	cur.execute("""
		INSERT INTO errors (error_message)
		VALUES (?)
		""", (error_message))
	db.commit()

"""Function to retrieve error messages from the errors table"""
def get_error_message(db, error_id):
	cur = db.cursor()
	cur.execute("""
		SELECT *
		FROM errors
		WHERE error_id=?
		""", (error_id,))
	return cur.fetchall()

# Functions to interact with habits table
"""Function to add a new habit to habits table
	Parameters:
		- Task and periodicity are entered by the user.
		- The creation date is set to the current date by default in the database.
		- created_by is set to 'user' by default.
		- is_active is set to 1 by default."""
def add_habit(db, task, periodicity):
	cur = db.cursor()
	cur.execute("""
		INSERT INTO habits (task, periodicity)
		VALUES (?, ?)
		""", (task, periodicity))
	db.commit()

"""Function to update an habit in habits table
	Parameters:
		- task and periodicity are entered by the user.
		- habit_id: the unique identifier of the habit to be deleted."""
def update_habit(db, habit_id, task, periodicity):
	cur = db.cursor()
	cur.execute("""
		UPDATE habits
		SET task = ?, periodicity = ?, updated_on = date('now')
		WHERE habit_id = ?;
		""", (task, periodicity, habit_id))
	db.commit()

"""Function to deactivate an habit in habits table. User wishes to deleted an habit, is_active is set to 0 in the database.
	Parameters:
		- habit_id: the unique identifier of the habit to be deleted."""
def delete_habit(db, habit_id):
	cur = db.cursor()
	cur.execute("""
		UPDATE habits
		SET deleted_on = date('now'), is_active = 0
		WHERE habit_id = ?;
		""", (habit_id,))
	db.commit()

# Function to interact with checkoff table
"""Function to mark a habit as completed. Add a new record in checkoffs table. The date is set to the current date by default in the database.
	Parameters:
		- habit_id: the unique identifier of the habit to be checked off."""
def add_checkoff(db, habit_id):
	cur = db.cursor()
	cur.execute("""
		INSERT INTO checkoffs (habit_id)
		VALUES (?)
		""", (habit_id,))
	db.commit()

# Functions te retrieve lists of habits for analysis
"""Function to retrieve a list of all active tracked habits (is_active = 1) from the habits table created by user (created_by = user)."""
def get_all_habits(db):
	cur = db.cursor()
	cur.execute("""
		SELECT *
		FROM habits
		WHERE created_by = ? AND is_active = ?
		""", ('user', 1))
	return cur.fetchall()

"""Function to retrieve a list of all predefined habits from the habits table."""
def get_demo_tracking(db):
	cur = db.cursor()
	cur.execute("""
		SELECT * 
		FROM habits 
		WHERE created_by = ? AND is_active = ?
		""", ('predefined', 0))
	return cur.fetchall()