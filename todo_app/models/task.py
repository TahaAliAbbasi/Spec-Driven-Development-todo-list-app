"""
Task model for the Console Todo Application.

This module defines the Task entity with its attributes and basic operations.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with id, title, description, and completion status.

    Attributes:
        id: Sequential identifier starting from 1
        title: Task title with non-empty validation
        description: Optional task description, may be empty
        is_completed: Completion status, defaults to False
    """
    id: int
    title: str
    description: Optional[str] = ""
    is_completed: bool = False

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")
        if not isinstance(self.is_completed, bool):
            raise ValueError("Task completion status must be a boolean")

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.is_completed = False

    def toggle_completion(self) -> None:
        """Toggle the completion status of the task."""
        self.is_completed = not self.is_completed

    def update_title(self, new_title: str) -> None:
        """Update the task title with validation.

        Args:
            new_title: The new title for the task

        Raises:
            ValueError: If the new title is empty or whitespace-only
        """
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")
        self.title = new_title

    def update_description(self, new_description: str) -> None:
        """Update the task description.

        Args:
            new_description: The new description for the task
        """
        self.description = new_description if new_description is not None else ""

    def to_dict(self) -> dict:
        """Convert the task to a dictionary representation.

        Returns:
            Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_completed': self.is_completed
        }

    def get_display_with_emoji(self) -> str:
        """
        Get a display string for the task with emoji indicator.

        Returns:
            Formatted string with emoji and task information
        """
        emoji = "✓" if self.is_completed else "✗"
        if self.description:
            return f"{emoji} {self.title} - {self.description}"
        else:
            return f"{emoji} {self.title}"