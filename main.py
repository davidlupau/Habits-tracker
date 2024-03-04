# Description: This is the main file for the MindMold program. It will be the file that the user runs to interact with the program.
import sys
from habit import prompt_for_task, prompt_for_periodicity, check_habit_continuity, get_task_periodicity
from analysis import display_habit_list, display_demo_tracking
import db
from error_handler import error_2, error_3, error_4, error_5

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


# Call function to create the database and the tables if they don't exist
db.get_db(name="main.db")

# Check if predefined habits have already been created. If not, create them.
check_predefined_habits = get_demo_tracking(db)
if len(check_predefined_habits) == 0:
    db.insert_predefined_habits(db)

# Main program
# Display the main menu with a welcome message and prompt the user for a choice
print("Welcome to MindMold. Mold your mind and body into their best versions with MindMold – habit tracking made easy! \n")
print("You've taken the first step towards transforming your life, one habit at a time. What's on the agenda today?")
user_choice = main_menu()

if user_choice == 1:
    # Create a new habit
    print("You chose to create a new habit. Enter the name of the habit and press enter: ")
    task = self.prompt_for_task()
    periodicity = self.prompt_for_periodicity()

    # Call a function that add the habit to the database and return the habit_id of the newly created habit
    habit_id = db.add_habit(db, task, periodicity,)

    # Get the habit_id of the new habit to initiate the streak in streak table and add a checkoff in checkoffs table
    db.start_streak(db, habit_id)
    db.add_checkoff(db, habit_id)

    print(f"New habit '{task}' created successfully!\n")

    # Prompt the user to press Enter to continue
    return_to_menu()

elif user_choice == 2:
    # View your habits
    print("You chose to view your habits.")
    self.display_habit_list()

    # Prompt the user to press Enter to continue
    return_to_menu()

elif user_choice == 3:
    # Update a habit
    # Retrieve and display the list of active habits
    print("You chose to update a habit. Here are your current habits:")
    db.display_habit_list(db)

    # User is asked to choose a habit to update
    print("Which habit would you like to update? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        #Retrieve habit name and periodicity
        task_name, periodicity = self.get_task_periodicity(db, habit_id)
        print(f"You chose to update habit {habit_id}, {task_name}. The periodicity is {periodicity}.")

        # Prompt the user for the new task name
        print("Do you want to change the name of the habit? Enter 1 for yes, 2 for no")
        choice = get_int_choice()
        if choice == 1:
            new_task = self.prompt_for_task()
        elif choice == 2:
            new_task = task_name
        else:
            print(error_5.get_error_message())

        # Prompt the user for the periodicity
        print("Do you want to change the periodicity of the habit? Enter 1 for yes, 2 for no")
        choice = get_int_choice()
        if choice == 1:
            new_periodicity = self.prompt_for_periodicity()
        elif choice == 2:
            new_periodicity = periodicity
        else:
            print(error_5.get_error_message())

        # Call a function to update the habit in the database
        db.update_habit(db, habit_id, new_task, new_periodicity)
        print(f"Habit {habit_id} updated successfully!\n")
        # Prompt the user to press Enter to continue
        return_to_menu()

    else:
        print(error_3.get_error_message())


elif user_choice == 4:
    # Mark a habit as completed
    print("You chose to mark a habit as completed. Here are your current habits:")
    db.display_habit_list(db)

    # User is asked to choose a habit to mark as completed
    print("Which habit would you like to mark as completed? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        #Retrieve habit name and periodicity
        task_name, periodicity = self.get_task_periodicity(db, habit_id)
        print(f"You chose to mark habit {habit_id}, {task_name} as completed. The periodicity is {periodicity}. Are you sure you want to proceed? Enter 1 for yes, 2 for no")

        choice = get_int_choice()
        if choice == 1:
            # Call a function to check if the habit is broken
            habit_continuity = self.check_habit_continuity(habit_id)
            if habit_continuity == True:
                # Call a function to add a checkoff in the checkoffs table
                db.add_checkoff(db, habit_id)
                db.increment_current_streak(db, habit_id)
                print(f"Well done. Your streak is still active. Habit {habit_id} mark as completed successfully!\n")
                # Prompt the user to press Enter to continue
                return_to_menu()
            else:
                # Call a function to add a checkoff in the checkoffs table, end the current streak and start a new one
                db.add_checkoff(db, habit_id)
                db.end_streak(db, habit_id)
                db.start_streak(db, habit_id)
                print(f"Oops! It seems that you missed a checkoff but you've completed your habit and started a new streak. Habit {habit_id} mark as completed successfully!\n")
        elif choice == 2:
            print("Habit completion not updated.")
            # Prompt the user to press Enter to continue
            return_to_menu()
        else:
            print(error_5.get_error_message())

    else:
        print(error_3.get_error_message())

elif user_choice == 5:
    # Delete a habit
    print("You chose to delete a habit. Here is a list of your current habits:")
    db.display_habit_list(db)

    # User is asked to choose a habit to delete
    print("Which habit would you like to delete? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        #Retrieve habit name and periodicity
        task_name, periodicity = self.get_task_periodicity(db, habit_id)
        print(f"You chose to delete habit {habit_id}, {task_name}. The periodicity is {periodicity}. Are you sure you want to delete this habit? Enter 1 for yes, 2 for no")

        choice = get_int_choice()
        if choice == 1:
            db.delete_habit(db, habit_id)
            print(f"Habit {habit_id} deleted successfully!\n")
            # Prompt the user to press Enter to continue
            return_to_menu()
        elif choice == 2:
            print("Habit not deleted.")
            # Prompt the user to press Enter to continue
            return_to_menu()
        else:
            print(error_5.get_error_message())

    else:
        print(error_3.get_error_message())

    # User is asked to choose a habit to delete
    print("Which habit would you like to delete? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        #Retrieve habit name and periodicity
        task_name, periodicity = self.get_task_periodicity(db, habit_id)
        print(f"You chose to delete habit {habit_id}, {task_name}. The periodicity is {periodicity}. Are you sure you want to delete this habit? Enter 1 for yes, 2 for no")

        choice = get_int_choice()
        if choice == 1:
            db.delete_habit(db, habit_id)
            print(f"Habit {habit_id} deleted successfully!\n")
            # Prompt the user to press Enter to continue
            return_to_menu()
        elif choice == 2:
            print("Habit not deleted.")
            # Prompt the user to press Enter to continue
            return_to_menu()
        else:
            print(error_5.get_error_message())

    else:
        print(error_3.get_error_message())

elif user_choice == 6:
    # Analyze your habits
    pass

elif user_choice == 7:
    # See a demo of how MindMold works: analysis of predefined habits. Display list of predefined habits
    print("You chose to see a demo of how MindMold works. Here are the predefined habits:")
    self.display_demo_tracking(db)

    # Prompt the user to press Enter to continue
    input("Press Enter to continue...")

    # Prompt the user to press Enter to continue

