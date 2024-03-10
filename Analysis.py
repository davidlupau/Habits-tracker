from db import get_all_habits, get_longest_streak_all_habits, get_habit_details, get_longest_streak_one_habit, get_habits_by_periodicity

class Analysis:

    def display_habit_list(self, db, created_by, is_active):
        """Method to display the list of habits retrieved from the database.
        Parameter:
            - created_by ('user' or 'predefined')
            - is_active (1 if created by user, 0 if predefined).
        The method get_all_habits is called from the db module to retrieve the list of habits (a tuple of lists)."""
        habit_list = get_all_habits(db, created_by, is_active)
        for habit in habit_list:
            # Access the habit id
            habit_id = habit[0]
            print("Habit # ", habit_id)

            # Access the task name
            task_name = habit[1]
            print("Task Name:", task_name)

            # Access the periodicity
            periodicity = habit[2]
            print("Periodicity:", periodicity)

            # Access the creation date
            creation_date = habit[3]
            print("Creation Date:", creation_date)

            # Access the creation date
            update_date = habit[4]
            print("Last update on:", update_date, "\n")

        print("End of list.")

    def display_longest_streak_all_habits(self, db, created_by, is_active):
        """Method to display the longest streak of all habits (active and inactive).
        The method get_longest_streak_all_habits is called from the db module to retrieve the longest streak of all habits.
        The method get_habit_details is called from the db module to retrieve name and periodicity of the habit with the longest streak to display complete information.
        The information is then displayed to the user.
        Parameters:
            - created_by ('user' or 'predefined')
            - is_active (1 if created by user, 0 if predefined)."""
        # Get the longest streak of all habits
        longest_streak = get_longest_streak_all_habits(db, created_by, is_active)

        # Get the habit details
        habit_id = longest_streak[0]
        habit_details = get_habit_details(habit_id, db, created_by, is_active)

        # Access the periodicity to display the correct information
        if habit_details[2] == "daily":
            periodicity = "day(s)"
        elif habit_details[2] == "weekly":
            periodicity = "week(s)"
        elif habit_details[2] == "monthly":
            periodicity = "month(s)"

        # Display all information regarding the longest streak
        if longest_streak[3] is None:
            print(f"The longest streak of all habits is habit #", longest_streak[0], ", ", habit_details[1], "is", longest_streak[1], " ", {periodicity}, ". It started on", longest_streak[2], "and is still ongoing.\n")
        else:
            print(f"The longest streak of all habits is habit #", longest_streak[0], ", ", habit_details[1], "is", longest_streak[1], " ", {periodicity}, ". It started on", longest_streak[2], "and ended on", longest_streak[3], "\n")

    def display_longest_streak_one_habit(self, db, habit_id, created_by, is_active):
        """Method to display the longest streak of a specific habit. habit_id is entered by the user.
        The method get_longest_streak_one_habit is called from the db module to retrieve the longest streak of the habit.
        The information is then displayed to the user.
        Parameter:
            - habit_id: the unique identifier of the habit.
            - created_by ('user' or 'predefined')
            - is_active (1 if created by user, 0 if predefined)."""
        streak = get_longest_streak_one_habit(db, habit_id, created_by, is_active)

        # Get the habit details
        habit_details = get_habit_details(db, habit_id, created_by, is_active)

        # Access the periodicity to display the correct information
        if habit_details[2] == "daily":
            periodicity = "day(s)"
        elif habit_details[2] == "weekly":
            periodicity = "week(s)"
        elif habit_details[2] == "monthly":
            periodicity = "month(s)"

        if streak is not None:
            # If there is no end date, the streak is still ongoing
            if streak[3] is None:
                print(f"Longest streak for habit #", habit_id, ", ", habit_details[1], "is", streak[1], " ", {periodicity}, ". It started on", streak[2], "and is still ongoing.\n")
            else:
                print(f"Longest streak for habit #", habit_id, ", ", habit_details[1], "is", streak[1], " ", {periodicity}, ". It started on", streak[2], "and ended on", streak[3], "\n")
        else:
            print(f"No streak data available for habit #{habit_id}.")


    def display_habits_by_periodicity(self, db, periodicity, created_by, is_active):
        """Method to display the list of habits by periodicity.
        The method get_all_habits is called from the db module to retrieve the list of habits (a tuple of lists).
        The list is then filtered by periodicity and displayed to the user.
        Parameter:
            - periodicity # daily, weekly, monthly
            - created_by ('user' or 'predefined')
            - is_active (1 if created by user, 0 if predefined).
        Returns the list of habits with the requested periodicity."""
        habit_list = get_habits_by_periodicity(db, periodicity, created_by, is_active)

        for habit in habit_list:
            # Access the habit id
            habit_id = habit[0]
            print("Habit # ", habit_id)

            # Access the task name
            task_name = habit[1]
            print("Task Name:", task_name)

            # Access the periodicity
            periodicity = habit[2]
            print("Periodicity:", periodicity)

            # Access the creation date
            creation_date = habit[3]
            print("Creation Date:", creation_date)

            # Access the creation date
            update_date = habit[4]
            print("Last update on:", update_date, "\n")