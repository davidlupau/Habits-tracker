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
		ended_on DATE,
		current_streak INTEGER DEFAULT 0,
    	is_active INTEGER DEFAULT 1,
		FOREIGN KEY(habit_id) REFERENCES habits(habit_id));""")

	db.commit()

# Functions to interact with habits table
def insert_predefined_habits(db):
    """Insert predefined habits into the database.
    Parameters:
    	task, periodicity, created_by, is_active are predefined and entered by the developer."""
	cur = db.cursor()

	predefined_habits = [
        ('Meditate', 'daily', 'predefined', 0),
        ('Learn German (5 minutes)', 'daily', 'predefined', 0),
        ('Go for a 10 km run', 'weekly', 'predefined', 0),
        ('Cook a new healthy recipe', 'weekly', 'predefined', 0),
        ('Send 100 euros to kids save account', 'monthly', 'predefined', 0),
        ('Read a full book', 'monthly', 'predefined', 0),
    ]

	cur.executemany("""INSERT INTO habits (task, periodicity, created_by, is_active)
		VALUES (?, ?, ?, ?)
		""", predefined_habits)

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
	"""Function to update an habit in habits table
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
	"""Function to deactivate an habit in habits table. User wishes to deleted an habit, is_active is set to 0 in the database.
	Parameters:
		- habit_id: the unique identifier of the habit to be deleted."""
	cur = db.cursor()
	cur.execute("""
		UPDATE habits
		SET deleted_on = date('now'), is_active = 0
		WHERE habit_id = ?;
		""", (habit_id,))
	db.commit()

def get_habit_details(db, habit_id):
    """Retrieve details of a habit based on habit_id.
    Parameters:
    	- habit_id: The unique identifier of the habit.
    Returns: A tuple containing the habit details such as name, periodicity, and other relevant information."""
    cur = db.cursor()
    cur.execute("""
        SELECT habit_id, task, periodicity, created_by, created_on, is_active
        FROM habits
        WHERE habit_id = ?;
        """, (habit_id,))
    return cur.fetchone()

# Function to interact with checkoff table
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

# Functions to retrieve lists of habits for analysis
def get_all_habits(db):
	"""Function to retrieve a list of all active tracked habits (is_active = 1) from the habits table created by user (created_by = user)."""
	cur = db.cursor()
	cur.execute("""
		SELECT *
		FROM habits
		WHERE created_by = ? AND is_active = ?
		""", ('user', 1))
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

def get_habits_by_periodicity(db, periodicity):
	"""Function that retrieves list of active tracked habits (is_active = 1) by periodicity.
	Parameters:
	- periodicity is selected by the user (daily, weekly or monthly)."""
	cur = db.cursor()
	cur.execute("""
		SELECT *
		FROM habits
		WHERE created_by = ? AND is_active = ?
		""", (periodicity, 1))
	return cur.fetchall()

def get_demo_tracking(db):
	"""Function to retrieve a list of all predefined habits from the habits table."""
	cur = db.cursor()
	cur.execute("""
		SELECT * 
		FROM habits 
		WHERE created_by = ? AND is_active = ?
		""", ('predefined', 0))
	return cur.fetchall()

# Functions to interact with streak table.
def start_streak(db, habit_id):
	"""Function to add a new record to the streak table when a new habit is created by user
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

def get_longest_streak_all_habits(db):
	"""Function to retrieve the longest streak of all habits. Returns habit_id, streak, start and end dates."""
	cur = db.cursor()
	cur.execute("""
		SELECT habit_id, current_streak, started_on, ended_on
		FROM streaks
		ORDER BY current_streak DESC
        LIMIT 1;
        """,)
	return cur.fetchone()

def get_longest_streak_one_habit(db, habit_id):
	"""Function to retrieve the longest streak of a specific habit requested by user. Returns habit_id, streak, start and end dates.
	Parameter:
		- habit_id: the unique identifier of the habit user wants the longest streak for."""
	cur = db.cursor()
	cur.execute("""
		SELECT habit_id, current_streak, started_on, ended_on
		FROM streaks
		WHERE habit_id = ? AND is_active = 1
		ORDER BY current_streak DESC
        LIMIT 1;
        """,(habit_id,))
	return cur.fetchone()