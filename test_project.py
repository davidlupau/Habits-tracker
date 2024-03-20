from habit import Habit
from db import get_db, add_habit, start_streak, increment_current_streak, add_checkoff, get_habit_details, delete_habit, get_longest_streak_one_habit, get_longest_streak_all_habits, get_habits_by_periodicity, update_habit, end_streak


class Testing:

    # Initialize the database connection
    def setup_method(self):
        self.db = get_db("test.db")

        # Create two habits and start streaks
        habit_id_1 = add_habit(self.db, "test habit 1", "daily", created_on="2024-02-17")
        start_streak(self.db, habit_id_1, started_on="2024-02-17")
        increment_current_streak(self.db, habit_id_1)
        increment_current_streak(self.db, habit_id_1)
        increment_current_streak(self.db, habit_id_1)
        increment_current_streak(self.db, habit_id_1)
        increment_current_streak(self.db, habit_id_1)
        increment_current_streak(self.db, habit_id_1)
        add_checkoff(self.db, habit_id_1, checkedoff_on="2024-02-17")
        add_checkoff(self.db, habit_id_1, checkedoff_on="2024-02-18")
        add_checkoff(self.db, habit_id_1, checkedoff_on="2024-02-19")
        add_checkoff(self.db, habit_id_1, checkedoff_on="2024-02-20")
        add_checkoff(self.db, habit_id_1, checkedoff_on="2024-02-21")
        add_checkoff(self.db, habit_id_1, checkedoff_on="2024-02-22")

        habit_id_2 = add_habit(self.db, "test habit 2", "weekly", created_on="2024-01-17")
        start_streak(self.db, habit_id_2, started_on="2024-01-17")
        increment_current_streak(self.db, habit_id_2)
        increment_current_streak(self.db, habit_id_2)
        increment_current_streak(self.db, habit_id_2)
        increment_current_streak(self.db, habit_id_2)
        add_checkoff(self.db, habit_id_2, checkedoff_on="2024-01-17")
        add_checkoff(self.db, habit_id_2, checkedoff_on="2024-01-24")
        add_checkoff(self.db, habit_id_2, checkedoff_on="2024-01-31")
        add_checkoff(self.db, habit_id_2, checkedoff_on="2024-02-07")

    def test_habit(self):
        # Check habit_1 continuity (should be broken)
        continuity = Habit()
        habit_continuity = continuity.check_habit_continuity(self.db, self.habit_id_1, 'user', 1)
        assert habit_continuity == False

        # Check habit_1 periodicity (should be daily)
        periodicity = Habit()
        habit_periodicity = periodicity.get_task_periodicity(self.db, self.habit_id_1, 'user', 1)
        assert habit_periodicity[1] == "daily"

    def test_db(self):
        # Check if habit 1 is being correctly updated
        update_habit(self.db, self.habit_id_1, "test habit 1 updated", "daily")
        habit_1_details = get_habit_details(self.db, self.habit_id_1, "user", 1)
        assert habit_1_details[1] == "test habit 1 updated"

        # Check if ending the streak of habit 2 is being correctly updated
        end_streak(self.db, self.habit_id_2)
        habit_2_streak = get_longest_streak_one_habit(self.db, self.habit_id_2, "user", 0)
        assert habit_2_streak is not None

        # Check if habit 2 is being correctly deleted (marked as inactive in the database)
        delete_habit(self.db, self.habit_id_2)
        habit_2_details = get_habit_details(self.db, self.habit_id_2, "user", 0)
        assert habit_2_details[5] == 0

    def test_analysis(self):
        # Check if the habit streaks are correctly updated
        habit_1_streak = get_longest_streak_one_habit(self.db, self.habit_id_1, "user", 1)
        current_streak = habit_1_streak[1]
        assert current_streak == 6

        # Check if the longest streak of all habits is correctly retrieved
        longest_streak_all = get_longest_streak_all_habits(self.db, "user", 1)
        assert longest_streak_all[0] == self.habit_id_1
        assert longest_streak_all[1] == 6

        # Check if the habit list is correctly retrieved
        habit_list = get_habits_by_periodicity(self.db, "daily", "user", 1)
        assert len(habit_list) == 1
        assert habit_list[0][0] == self.habit_id_1

    def teardown_method(self):
        import os
        os.remove("test.db")
