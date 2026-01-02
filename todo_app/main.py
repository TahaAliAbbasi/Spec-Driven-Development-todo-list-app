"""
Main entry point for the Console Todo Application.

This module implements the main menu loop and orchestrates
the application flow according to the UX contract.
"""
import sys
import os

# Add the parent directory to the Python path so imports work from within the todo_app directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.task_service import TaskService
from cli.menu import MenuHandler


def main():
    """
    Main function that runs the todo application.

    Implements the main loop behavior as specified in the Program Flow & State Lifecycle:
    1. Display main menu with numbered options
    2. Wait for user input
    3. Validate input and execute corresponding action
    4. Display results or error messages
    5. Return to main menu unless exit is selected
    6. Repeat until user chooses to exit
    """
    try:
        # Initialize services
        task_service = TaskService()
        menu_handler = MenuHandler(task_service)

        print("Welcome to the Todo Application!")

        # Main loop
        while True:
            # Display menu
            menu_handler.display_menu()

            # Get user input
            choice = input().strip()

            # Handle the choice and determine if we should continue
            should_continue = menu_handler.handle_menu_choice(choice)

            # If not continuing, exit the loop
            if not should_continue:
                break
    except KeyboardInterrupt:
        print("\nThank you for using the Todo Application. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print("Thank you for using the Todo Application. Goodbye!")


if __name__ == "__main__":
    main()