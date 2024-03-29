from error_handler import error_1, error_2
from db import last_checkedoff_on, get_habit_details
import datetime


class Habit:
    """Class to represent a habit
    Attributes:
        - task: The name of the habit
        - periodicity: The frequency at which the habit is to be performed
        - date: The date the habit was created
        - checkoffs: The number of times the habit has been performed
        - created_by: The user who created the habit.
    Methods:
        - __init__: Constructor to initialize the habit object
        - prompt_for_task: Method to prompt the user for the task name
        - prompt_for_periodicity: Method to prompt the user for the periodicity of the habit (daily, monthly, weekly)"""

    def __init__(self, habit_id=None, task=None, periodicity=None, date=None, checkoffs=0, created_by='user', is_active=True):
        self.habit_id = habit_id
        self.task = task
        self.periodicity = periodicity
        self.date = date
        self.checkoffs = checkoffs
        self.created_by = created_by
        self.is_active = is_active

    def prompt_for_task(self):
        """Method to prompt the user for the task name. Input is taken from the command line. If the input is empty, the user is prompted to try again."""
        print("Enter the name of the habit and press enter: ")
        task = input()
        if len(task) == 0:
            print(error_1.get_error_message())
            return self.prompt_for_task()
        return task

    def prompt_for_periodicity(self):
        """Method to prompt the user for the periodicity of the habit (1 for daily, 2 for monthly, 3 for weekly).
        Input is taken from the command line. If the input is invalid (different from 1, 2 or 3), the user is prompted to try again."""
        print("Choose a periodicity for the habit:\n"
              "Press 1 for daily\n"
              "Press 2 for weekly\n"
              "Press 3 for monthly\n"
              "Then press enter: ")
        periodicity = input()
        if periodicity == '1':
            return 'daily'
        elif periodicity == '2':
            return 'weekly'
        elif periodicity == '3':
            return 'monthly'
        else:
            print(error_2.get_error_message())
            return self.prompt_for_periodicity()


    def check_habit_continuity(self, db, habit_id, created_by, is_active):
        """Function to check if a habit is broken based on its periodicity and the last completion date.
        Parameters:
            - habit_id: the unique identifier of the habit to be checked off.
        The function retrieves the last completion date of the habit from the checkoffs table and compares it to the current date.
        Returns True if the habit is not broken and False if the habit is broken.
        The habit is considered broken if the difference between the last completion date and the current date is greater than the periodicity of the habit."""
        last_completion_date_str = last_checkedoff_on(db, habit_id)
        # Check if there is a last completion date
        if not last_completion_date_str:
            # If there is no last completion date, it's the first checkoff, so the habit is not broken
            return True

        habit_details = get_habit_details(db, habit_id, created_by, is_active)
        periodicity = habit_details[2]

        # Convert the last completion date from string to a datetime object
        last_completion_date = datetime.datetime.strptime(last_completion_date_str, '%Y-%m-%d').date()
        # Get the current date
        current_date = datetime.date.today()
        # Calculate the difference in days
        difference = (current_date - last_completion_date).days

        # Check if the habit is broken based on its periodicity
        if periodicity == 'daily' and difference >= 2:
            return False  # Habit is broken
        elif periodicity == 'weekly' and difference >= 8:
            return False  # Habit is broken
        elif periodicity == 'monthly':
            # For monthly, check if the month has changed beyond one month
            month_diff = (current_date.year - last_completion_date.year) * 12 + current_date.month - last_completion_date.month
            if month_diff >= 2:
                return False  # Habit is broken

        return True  # Habit is not broken

    def get_task_periodicity(self, db, habit_id, created_by, is_active):
        """Function to retrieve the task name and periodicity of a habit.
        Parameters:
            - habit_id: the unique identifier of the habit to be checked off.
            - created_by ('user' or 'predefined')
            - is_active (1 if created by user, 0 if predefined).
        Returns the task name and periodicity of the habit."""
        habit_details = get_habit_details(db, habit_id, created_by, is_active)
        task_name = habit_details[1]
        periodicity = habit_details[2]
        return task_name, periodicity