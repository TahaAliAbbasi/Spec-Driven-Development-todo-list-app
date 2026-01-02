"""
MenuHandler for the Console Todo Application.

This module handles the CLI interface and user interactions.
"""
from typing import Optional
from todo_app.services.task_service import TaskService
from todo_app.utils.styling import get_styled_task_display, get_heading_styled


class MenuHandler:
    """
    Handles the CLI menu interface and user interactions.

    Implements the flows for adding, viewing, updating, deleting,
    and marking tasks complete/incomplete according to the UX contract.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the MenuHandler with a task service.

        Args:
            task_service: The TaskService instance to use for operations
        """
        self.task_service = task_service

    def display_menu(self):
        """Display the main menu with numbered options."""
        print("\n" + get_heading_styled("TODO APPLICATION"))
        print(get_heading_styled("================"))
        print("1. Add Task")
        print("2. View Task List")
        print("3. Update/Edit Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("Choose an option (1-6):", end=" ")

    def add_task_flow(self):
        """Handle the add task flow according to the UX contract."""
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.")
                return

            description_input = input("Enter task description (press Enter to skip): ")
            description = description_input if description_input else ""

            task = self.task_service.add_task(title, description)
            emoji_status = "✓" if task.is_completed else "✗"
            print(f"Task added with ID {task.id} - Status: {emoji_status} {task.title}")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

    def view_tasks_flow(self):
        """Handle the view tasks flow according to the UX contract."""
        try:
            tasks = self.task_service.get_all_tasks()
            if not tasks:
                print("\nNo tasks found.")
                return

            print("\n" + get_heading_styled("TASK LIST:"))
            for task in tasks:
                styled_task = get_styled_task_display(task)
                print(f"{task.id}. {styled_task}")
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

    def update_task_flow(self):
        """Handle the update/edit task flow according to the UX contract."""
        try:
            task_id_input = input("Enter task ID to edit: ").strip()
            if not task_id_input.isdigit():
                print("Error: Please enter a valid task ID.")
                return

            task_id = int(task_id_input)
            if not self.task_service.validate_task_id(task_id):
                print(f"Error: Task with ID {task_id} does not exist.")
                return

            # Get current task values
            current_task = self.task_service.get_task_by_id(task_id)

            # Get new title (or keep current)
            new_title_input = input(f"Enter new title (current: '{current_task.title}', press Enter to keep): ")
            new_title = new_title_input if new_title_input else None

            # Get new description (or keep current)
            new_description_input = input(f"Enter new description (current: '{current_task.description}', press Enter to keep): ")
            new_description = new_description_input if new_description_input != "" else None

            # Update the task
            updated_task = self.task_service.update_task(task_id, new_title, new_description)
            if updated_task:
                emoji_status = "✓" if updated_task.is_completed else "✗"
                styled_task = get_styled_task_display(updated_task)
                print(f"Task {task_id} edited successfully - {styled_task}")
            else:
                print(f"Error: Task with ID {task_id} does not exist.")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

    def delete_task_flow(self):
        """Handle the delete task flow according to the UX contract."""
        try:
            task_id_input = input("Enter task ID to delete: ").strip()
            if not task_id_input.isdigit():
                print("Error: Please enter a valid task ID.")
                return

            task_id = int(task_id_input)
            if not self.task_service.validate_task_id(task_id):
                print(f"Error: Task with ID {task_id} does not exist.")
                return

            # Get the task before deletion to show its details
            task_to_delete = self.task_service.get_task_by_id(task_id)
            success = self.task_service.delete_task(task_id)
            if success:
                emoji_status = "✓" if task_to_delete.is_completed else "✗"
                print(f"Task {task_id} deleted successfully - Was: {emoji_status} {task_to_delete.title}")
            else:
                print(f"Error: Task with ID {task_id} does not exist.")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

    def mark_task_complete_flow(self):
        """Handle the mark task complete flow according to the UX contract."""
        try:
            task_id_input = input("Enter task ID to toggle completion status: ").strip()
            if not task_id_input.isdigit():
                print("Error: Please enter a valid task ID.")
                return

            task_id = int(task_id_input)
            if not self.task_service.validate_task_id(task_id):
                print(f"Error: Task with ID {task_id} does not exist.")
                return

            task = self.task_service.toggle_task_status(task_id)
            if task:
                status = "completed" if task.is_completed else "incomplete"
                emoji_status = "✓" if task.is_completed else "✗"
                print(f"Task {task_id} marked as {status} - Status: {emoji_status} {task.title}")
            else:
                print(f"Error: Task with ID {task_id} does not exist.")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

    def handle_menu_choice(self, choice: str) -> bool:
        """
        Handle a menu choice and return whether to continue.

        Args:
            choice: The user's menu choice

        Returns:
            True if the application should continue, False to exit
        """
        try:
            if choice == "1":
                self.add_task_flow()
            elif choice == "2":
                self.view_tasks_flow()
            elif choice == "3":
                self.update_task_flow()
            elif choice == "4":
                self.delete_task_flow()
            elif choice == "5":
                self.mark_task_complete_flow()
            elif choice == "6":
                print("Thank you for using the Todo Application. Goodbye!")
                return False
            else:
                print("Error: Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return False
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

        return True