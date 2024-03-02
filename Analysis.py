from db import get_all_habits, get_longest_streak_all_habits, get_habit_details, get_longest_streak_one_habit, get_demo_tracking

class analysis:

    def display_habit_list(self, db):
        """Method to display the list of habits retrieved from the database.
        The method get_all_habits is called from the db module to retrieve the list of habits (a tuple of lists)."""
        habit_list = get_all_habits(db)
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

    def display_longest_streak_all_habits(self, db):
        """Method to display the longest streak of all habits (active and inactive).
        The method get_longest_streak_all_habits is called from the db module to retrieve the longest streak of all habits.
        The method get_habit_details is called from the db module to retrieve name and periodicity of the habit with the longest streak to display complete information.
        The information is then displayed to the user."""
        # Get the longest streak of all habits
        longest_streak = get_longest_streak_all_habits(db)

        # Get the habit details
        habit_id = longest_streak[0]
        habit_details = get_habit_details(habit_id, db)

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

    def display_longest_streak_one_habit(self, db, habit_id):
        """Method to display the longest streak of a specific habit. habit_id is entered by the user.
        The method get_longest_streak_one_habit is called from the db module to retrieve the longest streak of the habit.
        The information is then displayed to the user."""
        streak = get_longest_streak_one_habit(db, habit_id)

        # Get the habit details
        habit_id = longest_streak[0]
        habit_details = get_habit_details(db, habit_id)

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

    def display_demo_tracking(self, db):
        """Method to display the list of predefined habits.
        The method get_demo_tracking is called from the db module to retrieve the list of predefined habits (a tuple of lists).
        The list is then displayed to the user."""
        demo_list = get_demo_tracking(db)

        for habit in demo_list:
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