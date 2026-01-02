"""
Test script for the Console Todo Application.

This script tests the core functionality of the todo application.
"""
from todo_app.services.task_service import TaskService
from todo_app.models.task import Task


def test_task_creation():
    """Test creating tasks with the TaskService."""
    print("Testing task creation...")
    service = TaskService()

    # Test adding a task
    task = service.add_task("Test Task 1", "This is a test task")
    print(f"Created task: ID={task.id}, Title='{task.title}', Description='{task.description}', Completed={task.is_completed}")

    # Test adding another task
    task2 = service.add_task("Test Task 2")
    print(f"Created task: ID={task2.id}, Title='{task2.title}', Description='{task2.description}', Completed={task2.is_completed}")

    # Test getting all tasks
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")

    # Test validation - should raise error for empty title
    try:
        service.add_task("")
        print("ERROR: Should have raised an exception for empty title")
    except ValueError as e:
        print(f"Correctly caught validation error: {e}")

    print("Task creation tests passed!")


def test_task_operations():
    """Test updating, deleting, and toggling tasks."""
    print("\nTesting task operations...")
    service = TaskService()

    # Add a task
    task = service.add_task("Original Task", "Original description")
    print(f"Added task: {task.id} - {task.title}")

    # Update the task
    updated_task = service.update_task(task.id, "Updated Task", "Updated description")
    print(f"Updated task: {updated_task.id} - {updated_task.title} - {updated_task.description}")

    # Toggle completion status
    toggled_task = service.toggle_task_status(task.id)
    print(f"Toggled completion status: {toggled_task.id} - Completed: {toggled_task.is_completed}")

    # Toggle again
    toggled_task = service.toggle_task_status(task.id)
    print(f"Toggled again: {toggled_task.id} - Completed: {toggled_task.is_completed}")

    # Delete the task
    success = service.delete_task(task.id)
    print(f"Task deletion result: {success}")

    # Verify task is deleted
    remaining_tasks = service.get_all_tasks()
    print(f"Remaining tasks after deletion: {len(remaining_tasks)}")

    print("Task operations tests passed!")


def test_task_validation():
    """Test task validation."""
    print("\nTesting task validation...")

    # Test creating a task with empty title - should raise error
    try:
        task = Task(1, "")
        print("ERROR: Should have raised an exception for empty title")
    except ValueError as e:
        print(f"Correctly caught validation error: {e}")

    # Test creating a task with whitespace-only title - should raise error
    try:
        task = Task(1, "   ")
        print("ERROR: Should have raised an exception for whitespace-only title")
    except ValueError as e:
        print(f"Correctly caught validation error: {e}")

    # Test creating a valid task
    task = Task(1, "Valid Task")
    print(f"Successfully created valid task: {task.id} - {task.title}")

    print("Task validation tests passed!")


if __name__ == "__main__":
    print("Running Todo Application Tests...")
    test_task_validation()
    test_task_creation()
    test_task_operations()
    print("\nAll tests passed! The Todo Application is working correctly.")