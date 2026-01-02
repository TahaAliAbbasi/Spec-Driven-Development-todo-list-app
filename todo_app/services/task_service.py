"""
TaskService for the Console Todo Application.

This module provides business logic for task operations including
adding, retrieving, updating, deleting, and toggling completion status.
"""
from typing import Dict, List, Optional
from todo_app.models.task import Task


class TaskService:
    """
    Service class for managing tasks with business logic.

    Implements operations for adding, retrieving, updating, deleting,
    and toggling completion status of tasks with validation.
    """

    def __init__(self):
        """Initialize the TaskService with an empty task collection."""
        self.tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and optional description.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The created Task object with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Validate title is not empty
        if not title or not title.strip():
            raise ValueError("Error: Task title cannot be empty.")

        # Create task with next available ID
        task = Task(id=self._next_id, title=title.strip(), description=description, is_completed=False)
        self.tasks[self._next_id] = task

        # Increment ID for next task
        self._next_id += 1

        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection.

        Returns:
            A list of all Task objects
        """
        return list(self.tasks.values())

    def get_completed_tasks(self) -> List[Task]:
        """
        Retrieve all completed tasks.

        Returns:
            A list of completed Task objects
        """
        return [task for task in self.tasks.values() if task.is_completed]

    def get_incomplete_tasks(self) -> List[Task]:
        """
        Retrieve all incomplete tasks.

        Returns:
            A list of incomplete Task objects
        """
        return [task for task in self.tasks.values() if not task.is_completed]

    def update_task(self, task_id: int, new_title: Optional[str] = None,
                    new_description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            new_title: New title (optional, keeps current if None)
            new_description: New description (optional, keeps current if None)

        Returns:
            The updated Task object if successful, None if task not found

        Raises:
            ValueError: If new_title is empty or whitespace-only
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        # Update title if provided
        if new_title is not None:
            if new_title == "":  # Empty string means clear the title
                if not new_title.strip():
                    raise ValueError("Error: Task title cannot be empty.")
            else:
                task.update_title(new_title)

        # Update description if provided
        if new_description is not None:
            task.update_description(new_description)

        return task

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if successful, None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.toggle_completion()
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if task not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def validate_task_id(self, task_id: int) -> bool:
        """
        Check if a task ID exists in the collection.

        Args:
            task_id: The ID to validate

        Returns:
            True if the ID exists, False otherwise
        """
        return task_id in self.tasks

    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            The next sequential ID
        """
        return self._next_id