# Import error messages from error_handler.py
from error_handler import error_1, error_2


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

    def __init__(self, task, periodicity, date, checkoffs, created_by):
        self.task = task
        self.periodicity = periodicity
        self.date = date
        self.checkoffs = checkoffs
        self.created_by = created_by

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