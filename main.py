# Description: This is the main file for the MindMold program. It will be the file that the user runs to interact with the program.
from habit import Habit
from analysis import Analysis
import db
from functions_main import main_menu, get_int_choice, return_to_menu, habits_list, task_periodicity
from error_handler import error_3, error_4, error_5


if --name-- == "--main--":
    cli()


# Main program
# Display the main menu with a welcome message and prompt the user for a choice
print("Welcome to MindMold. Mold your mind and body into their best versions with MindMold – habit tracking made easy! \n")
print("You've taken the first step towards transforming your life, one habit at a time. What's on the agenda today?")
user_choice = main_menu()

if user_choice == 1:
    # Create a new habit
    print("You chose to create a new habit. Enter the name of the habit and press enter: ")
    habit_prompts = Habit()
    task = habit_prompts.prompt_for_task()
    periodicity = habit_prompts.prompt_for_periodicity()

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
    habits_list(db, 'user', 1)

    # Prompt the user to press Enter to continue
    return_to_menu()

elif user_choice == 3:
    # Update a habit
    # Retrieve and display the list of active habits
    print("You chose to update a habit. Here are your current habits:")
    habits_list(db, 'user', 1)

    # User is asked to choose a habit to update
    print("Which habit would you like to update? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        # Create a new instance of the Habit class to prompt the user for the new task name and periodicity
        habit_prompts = Habit()
        # Retrieve habit name and periodicity
        task_name, periodicity = task_periodicity(db, habit_id, 'user', 1)
        print(f"You chose to update habit {habit_id}, {task_name}. The periodicity is {periodicity}.")

        # Prompt the user for the new task name
        print("Do you want to change the name of the habit? Enter 1 for yes, 2 for no")
        choice = get_int_choice()
        if choice == 1:
            new_task = habit_prompts.prompt_for_task()
        elif choice == 2:
            new_task = task_name
        else:
            print(error_5.get_error_message())

        # Prompt the user for the periodicity
        print("Do you want to change the periodicity of the habit? Enter 1 for yes, 2 for no")
        choice = get_int_choice()
        if choice == 1:
            new_periodicity = habit_prompts.prompt_for_periodicity()
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
    habits_list(db, 'user', 1)

    # User is asked to choose a habit to mark as completed
    print("Which habit would you like to mark as completed? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        #Retrieve habit name and periodicity
        task_name, periodicity = task_periodicity(db, habit_id, 'user', 1)
        print(f"You chose to mark habit {habit_id}, {task_name} as completed. The periodicity is {periodicity}. Are you sure you want to proceed? Enter 1 for yes, 2 for no")

        # Create a new instance of the Habit class to check if the habit is broken
        continuity = Habit()
        choice = get_int_choice()
        if choice == 1:
            # Call a function to check if the habit is broken
            habit_continuity = continuity.check_habit_continuity(db, habit_id)
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
    habits_list(db, 'user', 1)

    # User is asked to choose a habit to delete
    print("Which habit would you like to delete? Enter the habit id and press enter:")
    habit_id = get_int_choice()
    active_habits = db.get_habit_ids(db)

    # Check if the habit_id entered by the user is valid
    if habit_id in active_habits:
        #Retrieve habit name and periodicity
        task_name, periodicity = task_periodicity(db, habit_id, 'user', 1)
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
        task_name, periodicity = task_periodicity(db, habit_id, 'user', 1)
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
    print("Let's see how you are doing. What would you like to analyze?")
    print("1. List of all habits with the same periodicity")
    print("2. Longest streak of all habits")
    print("3. Longest streak of a specific habit")
    user_choice = main_menu()

    if user_choice == 1:
        # List of all habits with the same periodicity
        print("You chose to list all habits with the same periodicity. Enter the periodicity (daily, weekly, monthly) and press enter:")
        prompt_periodicity = Habit()
        periodicity = prompt_periodicity.prompt_for_periodicity()
        habit_by_periodicity = Analysis()
        habit_by_periodicity.display_habits_by_periodicity(db, periodicity, 'user', 1)

        # Prompt the user to press Enter to continue
        return_to_menu()

    elif user_choice == 2:
        # Longest streak of all habits
        print("You chose to see the longest streak of all habits.")
        longest_streak = Analysis()
        longest_streak.display_longest_streak_all_habits(db, 'user', 1)

        # Prompt the user to press Enter to continue
        return_to_menu()

    elif user_choice == 3:
        # Longest streak of a specific habit
        print("You chose to see the longest streak of a specific habit. Here is a list of your current habits:")
        habits_list(db, 'user', 1)

        print("Which habit would you like to analyze? Enter the habit id and press enter:")
        habit_id = get_int_choice()
        active_habits = db.get_habit_ids(db)

        # Check if the habit_id entered by the user is valid
        if habit_id in active_habits:
            habit_streak = Analysis()
            habit_streak.display_longest_streak_one_habit(db, habit_id, 'user', 1)

            # Prompt the user to press Enter to continue
            return_to_menu()
        else:
            print(error_3.get_error_message())

    else:
        print(error_4.get_error_message())

elif user_choice == 7:
    # See a demo of how MindMold works: analysis of predefined habits. Display list of predefined habits
    print("You chose to see a demo of how MindMold works. MindMold can display a list of all your current active habits. Here is an example with a list of predefined habits:")
    habits_list(db, 'predefined', 0)

    # Prompt the user to press Enter to continue
    input("Press Enter to continue...")

    # Displays a list of predefined habits with daily periodicity
    print("MindMold can also display the list of all habits with the same periodicity. Here is an example with the list of all predefined habits with daily periodicity:")
    habit_by_periodicity = Analysis()
    habit_by_periodicity.display_habits_by_periodicity(db, 'daily', 'user', 1)

    # Prompt the user to press Enter to continue
    input("Press Enter to continue...")

    # Display the longest streak of all predefined habits
    print("MindMold can also display the longest streak of all habits. Here is an example with the longest streak of all predefined habits:")
    longest_streak = Analysis()
    longest_streak.display_longest_streak_all_habits(db, 'predefined', 0)

    # Prompt the user to press Enter to continue
    input("Press Enter to continue...")

    # Display the longest streak of a specific predefined habit
    print("MindMold can also display the longest streak of a specific habit. Here is an example with the longest streak of a specific predefined habit:")
    habit_streak = Analysis()
    habit_streak.display_longest_streak_one_habit(db, 3, 'predefined', 2)

    print("End of demo. You can now use MindMold to track your habits and analyze your progress. Good luck!")
    # Prompt the user to press Enter to continue
    return_to_menu()