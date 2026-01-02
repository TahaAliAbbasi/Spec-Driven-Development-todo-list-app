"""
Tests for the Console Todo Application.

This module tests the functionality of the todo app including
the new enhancements: emoji indicators, styling, and editing.
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path so imports work from within the todo_app directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo_app.models.task import Task
from todo_app.services.task_service import TaskService
from todo_app.utils.styling import get_emoji_status, get_colored_text, get_bold_text, get_styled_task_display


class TestTaskModel(unittest.TestCase):
    """Test cases for the Task model."""

    def test_task_creation_default_values(self):
        """Test that tasks are created with default values."""
        task = Task(id=1, title="Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "")
        self.assertFalse(task.is_completed)

    def test_task_creation_with_description(self):
        """Test that tasks can be created with a description."""
        task = Task(id=1, title="Test task", description="A test description")
        self.assertEqual(task.description, "A test description")

    def test_task_creation_completed(self):
        """Test that tasks can be created as completed."""
        task = Task(id=1, title="Test task", is_completed=True)
        self.assertTrue(task.is_completed)

    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(id=1, title="Test task")
        task.mark_complete()
        self.assertTrue(task.is_completed)

    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = Task(id=1, title="Test task", is_completed=True)
        task.mark_incomplete()
        self.assertFalse(task.is_completed)

    def test_toggle_completion(self):
        """Test toggling task completion status."""
        task = Task(id=1, title="Test task", is_completed=False)
        task.toggle_completion()
        self.assertTrue(task.is_completed)
        task.toggle_completion()
        self.assertFalse(task.is_completed)

    def test_update_title(self):
        """Test updating task title."""
        task = Task(id=1, title="Test task")
        task.update_title("New title")
        self.assertEqual(task.title, "New title")

    def test_update_description(self):
        """Test updating task description."""
        task = Task(id=1, title="Test task")
        task.update_description("New description")
        self.assertEqual(task.description, "New description")

    def test_get_display_with_emoji(self):
        """Test the emoji display method."""
        task = Task(id=1, title="Test task", is_completed=False)
        display = task.get_display_with_emoji()
        self.assertIn("✗", display)
        self.assertIn("Test task", display)

        task.mark_complete()
        display = task.get_display_with_emoji()
        self.assertIn("✓", display)
        self.assertIn("Test task", display)


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService."""

    def setUp(self):
        """Set up a fresh TaskService for each test."""
        self.service = TaskService()

    def test_add_task_defaults(self):
        """Test that added tasks have default values."""
        task = self.service.add_task("Test task")
        self.assertEqual(task.title, "Test task")
        self.assertFalse(task.is_completed)  # Should default to False

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_completed_tasks(self):
        """Test retrieving completed tasks."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        self.service.toggle_task_status(task1.id)
        completed_tasks = self.service.get_completed_tasks()
        self.assertEqual(len(completed_tasks), 1)
        self.assertTrue(completed_tasks[0].is_completed)

    def test_get_incomplete_tasks(self):
        """Test retrieving incomplete tasks."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        self.service.toggle_task_status(task1.id)
        incomplete_tasks = self.service.get_incomplete_tasks()
        self.assertEqual(len(incomplete_tasks), 1)
        self.assertFalse(incomplete_tasks[0].is_completed)

    def test_update_task(self):
        """Test updating a task."""
        task = self.service.add_task("Original task")
        updated_task = self.service.update_task(task.id, "Updated task")
        self.assertEqual(updated_task.title, "Updated task")

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.service.add_task("Task to delete")
        result = self.service.delete_task(task.id)
        self.assertTrue(result)
        self.assertIsNone(self.service.get_task_by_id(task.id))

    def test_validate_task_id(self):
        """Test validating a task ID."""
        task = self.service.add_task("Test task")
        self.assertTrue(self.service.validate_task_id(task.id))
        self.assertFalse(self.service.validate_task_id(999))


class TestStylingUtils(unittest.TestCase):
    """Test cases for styling utilities."""

    def test_get_emoji_status(self):
        """Test emoji status function."""
        self.assertEqual(get_emoji_status(True), "✓")
        self.assertEqual(get_emoji_status(False), "✗")

    def test_get_colored_text(self):
        """Test colored text function."""
        text = "Test text"
        colored = get_colored_text(text, "red")
        self.assertIn("\033[31m", colored)
        self.assertIn(text, colored)

    def test_get_bold_text(self):
        """Test bold text function."""
        text = "Test text"
        bold = get_bold_text(text)
        self.assertIn("\033[1m", bold)
        self.assertIn(text, bold)

    def test_get_styled_task_display(self):
        """Test styled task display."""
        task = Task(id=1, title="Test task", is_completed=False)
        styled = get_styled_task_display(task)
        self.assertIn("✗", styled)
        self.assertIn("Test task", styled)

        task.mark_complete()
        styled = get_styled_task_display(task)
        self.assertIn("✓", styled)
        self.assertIn("Test task", styled)


if __name__ == '__main__':
    unittest.main()