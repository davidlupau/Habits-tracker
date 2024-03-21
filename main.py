# Description: This is the main file for the MindMold program. It will be the file that the user runs to interact with the program.
from functions_main import cli, main_menu, handle_choice



if __name__ == '__main__':
    db = cli()


# Display the main menu with a welcome message and prompt the user for a choice
print("Welcome to MindMold. Mold your mind and body into their best versions with MindMold – habit tracking made easy! \n")
print("You've taken the first step towards transforming your life, one habit at a time. What's on the agenda today?")
user_choice = main_menu()
handle_choice(db, user_choice)
