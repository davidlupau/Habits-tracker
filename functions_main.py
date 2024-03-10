# This file contains the functions used in the main.py file.
import sys
from habit import Habit
from analysis import Analysis
from error_handler import error_2, error_4


def main_menu():
    """Function to display the main menu of the program. The user can choose between 8 options.
    The user is prompted to enter a number between 1 and 8. If the input is invalid, the user is prompted to try again.
    The function returns the user's choice. If the user chooses to quit the program, the program is terminated.
    If the user chooses any other valid option, the program continues to the next step."""
    print("What's on the agenda?")
    print("1. Create a new habit")
    print("2. View your habits")
    print("3. Update a habit")
    print("4. Mark a habit as completed")
    print("5. Delete a habit")
    print("6. Analyze your habits")
    print("7. See a demo of how MindMold works")
    print("8. Quit the program")
    print("What would you like to do next? Type the number of your choice. Let’s keep the momentum going!")
    while True:
        choice = input()
        try:
            int_choice = int(choice)
            if 1 <= int_choice <= 8:
                if int_choice == 8:
                    sys.exit("Thank you for using MindMold. Goodbye!")
                return int_choice
            else:
                raise ValueError
        except ValueError:
            print(error_4.get_error_message())


def get_int_choice():
    """Function to prompt the user for an integer input. If the input is invalid, the user is prompted to try again.
    The function returns the user's choice."""
    while True:
        try:
            choice = int(input())
            return choice
            break
        except ValueError:
            print(error_2.get_error_message())


def return_to_menu():
    """Function to prompt the user to press Enter to return to the main menu."""
    input("Press Enter to return to the main menu...")
    main_menu()


def habits_list(db, created_by, is_active):
    """Function to display the list of habits retrieved from the database.
    It calls the display_habit_list method from the Analysis class.
    Parameter:
        - created_by ('user' or 'predefined')
        - is_active (1 if created by user, 0 if predefined)."""
    analysis_habit_list = Analysis()
    analysis_habit_list.display_habit_list(db, created_by, is_active)


def task_periodicity(db, habit_id, created_by, is_active):
    task_periodicity = Habit()
    task_name, periodicity = task_periodicity.get_task_periodicity(db, habit_id, created_by, is_active)
    return task_name, periodicity
