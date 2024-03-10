import sqlite3


def get_db(name="main.db"):
	"""Create a database connection to the SQLite database specified by name"""
	db = sqlite3.connect(name)
	create_tables(db)
	return db


def create_tables(db):
	"""Create tables for errors messages, streaks, checkoffs and habits from the create_table_sql statement."""
	cursor = db.cursor()

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
		ended_on DATE DEFAULT NULL,
		current_streak INTEGER DEFAULT 0,
    	is_active INTEGER DEFAULT 1,
		FOREIGN KEY(habit_id) REFERENCES habits(habit_id));""")

	db.commit()

# Functions to interact with habits table
def insert_predefined_habits(db):
	"""Insert predefined habits into the database: 6 habits in Habits table and 2 streaks are entered in Streaks table.
    Parameters:
		task, periodicity, created_by, is_active and dates are predefined and entered by the developer."""
	cur = db.cursor()

	predefined_habits = [
        (1, 'Meditate', 'daily', 'predefined', '2024-01-10', '2024-01-31', 0),
        (2, 'Learn German (5 minutes)', 'daily', 'predefined', '2024-01-10', '2024-01-10', 0),
        (3, 'Go for a 10 km run', 'weekly', 'predefined', '2024-01-10', '2024-02-01', 0),
        (4, 'Cook a new healthy recipe', 'weekly', 'predefined', '2024-01-14', '2024-02-17', 0),
        (5, 'Send 100 euros to kids save account', 'monthly', 'predefined', '2024-01-10', '2024-01-28', 0),
        (6, 'Read a full book', 'monthly', 'predefined', '2024-01-13', '2024-01-13', 0),
    ]

	cur.executemany("""INSERT INTO habits (habit_id, task, periodicity, created_by, created_on, updated_on, is_active)
		VALUES (?, ?, ?, ?, ?, ?, ?
		""", predefined_habits)

	predefined_streaks = [
        (1, '2024-01-10', '2024-01-22', 12, 0),
        (2, '2024-02-01', None, 6, 1),
    ]

	cur.executemany("""INSERT INTO streaks (habit_id, started_on, ended_on, current_streak, is_active)
        VALUES (?, ?, ?, ?, ?)
        """, predefined_streaks)

	db.commit()

def add_habit(db, task, periodicity):
	"""Function to add a new habit to habits table. It returns habit_id of the new habit to be used in the streak table.
	Parameters:
		- Task and periodicity are entered by the user.
		- Periodicity is either daily, weekly, monthly
		- The creation date is set to the current date by default in the database.
		- created_by is set by default to 'user' when user creates habit and set to 'predefined' for predefined habits.
		- is_active is set to 1 by default."""
	cur = db.cursor()
	cur.execute("""
		INSERT INTO habits (task, periodicity)
		VALUES (?, ?)
		""", (task, periodicity))
	db.commit()
# Get the habit_id of the newly created habit
	habit_id = cur.lastrowid
	return habit_id

def update_habit(db, habit_id, task, periodicity):
	"""Function to update a habit in habits table
	Parameters:
		- task and periodicity are entered by the user.
		- habit_id: the unique identifier of the habit to be deleted."""
	cur = db.cursor()
	cur.execute("""
		UPDATE habits
		SET task = ?, periodicity = ?, updated_on = date('now')
		WHERE habit_id = ?;
		""", (task, periodicity, habit_id))
	db.commit()

def delete_habit(db, habit_id):
	"""Function to deactivate a habit in habits table. User wishes to delete a habit, is_active is set to 0 in the database.
	Parameters:
		- habit_id: the unique identifier of the habit to be deleted."""
	cur = db.cursor()
	cur.execute("""
		UPDATE habits
		SET deleted_on = date('now'), is_active = 0
		WHERE habit_id = ?;
		""", (habit_id,))
	db.commit()

def get_habit_details(db, habit_id, created_by, is_active):
	"""Retrieve details of a habit based on habit_id.
    Parameters:
    	- habit_id: The unique identifier of the habit.
    	- created_by: 'user' or 'predefined'
    	- is_active: 1 if created by user, 0 if predefined.
    Returns: A tuple containing the habit details such as name, periodicity, and other relevant information."""
	cur = db.cursor()
	cur.execute("""
        SELECT habit_id, task, periodicity, created_by, created_on, is_active
        FROM habits
        WHERE habit_id = ? AND created_by = ? AND is_active = ?;
        """, (habit_id, created_by, is_active))
	return cur.fetchone()

# Functions to interact with checkoff table
def add_checkoff(db, habit_id):
	"""Function to mark a habit as completed. Add a new record in checkoffs table. The date is set to the current date by default in the database.
	Parameters:
		- habit_id: the unique identifier of the habit to be checked off."""
	cur = db.cursor()
	cur.execute("""
		INSERT INTO checkoffs (habit_id)
			VALUES (?)
			""", (habit_id,))
	db.commit()

def last_checkedoff_on(db, habit_id):
	"""Function to retrieve the last checkedoff date of a habit.
	Returns the last checkedoff date of a habit from the checkoffs table.
	Parameters:
		- habit_id: the unique identifier of the habit to be checked off."""
	cur = db.cursor()
	cur.execute("""
		SELECT checkedoff_on
		FROM checkoffs
		WHERE habit_id = ?
		ORDER BY checkedoff_on DESC
		LIMIT 1;
		""", (habit_id,))
	return cur.fetchone()

# Functions to retrieve lists of habits for analysis
def get_all_habits(db, created_by, is_active):
	"""Function to retrieve a list of all active tracked habits (is_active = 1) from the habits table created by user (created_by = user).
	Parameters:
		- created_by: 'user' or 'predefined'
		- is_active: 1 if created by user, 0 if predefined."""
	cur = db.cursor()
	cur.execute("""
		SELECT *
		FROM habits
		WHERE created_by = ? AND is_active = ?
		""", (created_by, is_active))
	return cur.fetchall()

def get_habit_ids(db):
	"""Function to retrieve a list of all active tracked habits (is_active = 1) from the habits table created by user (created_by = user).
	Function returns a list of habit_id."""
	cur = db.cursor()
	cur.execute("""
		SELECT habit_id
		FROM habits
		WHERE created_by = ? AND is_active = ?
		""", ('user', 1))
	return cur.fetchall()

def get_habits_by_periodicity(db, periodicity, created_by, is_active):
	"""Function that retrieves list of active tracked habits by periodicity.
	Parameters:
		- periodicity is selected by the user (daily, weekly or monthly).
		- created_by: 'user' or 'predefined'
		- is_active: 1 if created by user, 0 if predefined.
	Returns a list of habits with the requested periodicity."""
	cur = db.cursor()
	cur.execute("""
		SELECT *
		FROM habits
		WHERE periodicity = ? AND created_by = ? AND is_active = ?
		""", (periodicity, created_by, is_active))
	return cur.fetchall()

# Functions to handle streaks.
def start_streak(db, habit_id):
	"""Function to add a new record to the streak table when a new habit is created by user or when user mark habit as completed after breaking it
	Parameters:
		- The creation date is set to the current date by default in the database.
		- habit_id will be used as foreign key to track the habit's streak. It is retrieved from add_habit function."""
	cur = db.cursor()
	cur.execute("""
		INSERT INTO streaks (habit_id, started_on)
		Values (?, date('now'));
		""", (habit_id))
	db.commit()

def increment_current_streak(db, habit_id):
	"""Function to update the current habit streak by adding 1 to integer in current_streak column
	Parameters:
		- habit_id: the unique identifier of the habit to be deleted."""
	cur = db.cursor()
	cur.execute("""
		UPDATE streaks
		SET current_streak = current_streak + 1
		WHERE habit_id = ? AND is_active = 1;
		""", (habit_id,))
	db.commit()

def end_streak(db, habit_id):
	"""Function to update the attribute is_active to 0 when habit is deleted or when user breaks the habit.
	Parameter:
		- habit_id: the unique identifier of the habit to be deleted."""
	cur = db.cursor()
	cur.execute("""
		UPDATE streaks
		SET is_active = 0, ended_on = date('now')
		WHERE habit_id = ? AND is_active = 1;
		""", (habit_id,))
	db.commit()

def get_longest_streak_all_habits(db, created_by, is_active):
	"""Function to retrieve the longest streak of all habits.
	Parameters:
		- created_by: 'user' or 'predefined'
		- is_active: 1 if created by user, 0 if predefined.
	Returns habit_id, streak, start and end dates."""
	cur = db.cursor()
	cur.execute("""
		SELECT habit_id, current_streak, started_on, ended_on
		FROM streaks
			WHERE habit_id IN (SELECT habit_id FROM habits WHERE created_by = ? AND is_active = ?)
		ORDER BY current_streak DESC
        LIMIT 1;
        """, (created_by, is_active))
	return cur.fetchone()

def get_longest_streak_one_habit(db, habit_id, created_by, is_active):
	"""Function to retrieve the longest streak of a specific habit. Returns habit_id, streak, start and end dates.
	Parameter:
		- habit_id: the unique identifier of the habit user wants the longest streak for.
		- created_by: 'user' or 'predefined'
		- is_active: 1 if created by user, 0 if predefined."""
	cur = db.cursor()
	cur.execute("""
		SELECT habit_id, current_streak, started_on, ended_on
		FROM streaks
		WHERE habit_id = ? AND created_by = ? AND is_active = ?
		ORDER BY current_streak DESC
        LIMIT 1;
        """,(habit_id, created_by, is_active))
	return cur.fetchone()