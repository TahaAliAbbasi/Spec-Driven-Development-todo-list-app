"""
Data transformation utility for converting SQLite data to PostgreSQL format.

This script transforms task data exported from SQLite to ensure compatibility
with PostgreSQL data types and constraints.
"""

from typing import List, Dict, Any
from datetime import datetime
import json


def transform_task_for_postgresql(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform a single task from SQLite format to PostgreSQL format.

    Args:
        task: Task dictionary from SQLite export

    Returns:
        Transformed task dictionary compatible with PostgreSQL
    """
    transformed = {
        "id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "is_completed": bool(task["is_completed"]),  # Ensure boolean type
        "created_at": task["created_at"],
        "updated_at": task["updated_at"]
    }

    # Validate and clean data
    if not transformed["title"] or not transformed["title"].strip():
        raise ValueError(f"Task {task['id']} has empty title")

    if len(transformed["title"]) > 255:
        print(f"Warning: Task {task['id']} title exceeds 255 characters, truncating")
        transformed["title"] = transformed["title"][:255]

    return transformed


def transform_tasks_batch(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transform a batch of tasks from SQLite to PostgreSQL format.

    Args:
        tasks: List of task dictionaries from SQLite

    Returns:
        List of transformed task dictionaries
    """
    transformed_tasks = []
    errors = []

    for task in tasks:
        try:
            transformed = transform_task_for_postgresql(task)
            transformed_tasks.append(transformed)
        except Exception as e:
            errors.append(f"Error transforming task {task.get('id', 'unknown')}: {e}")

    if errors:
        print("Transformation errors:")
        for error in errors:
            print(f"  - {error}")

    print(f"Successfully transformed {len(transformed_tasks)} out of {len(tasks)} tasks")
    return transformed_tasks


def load_tasks_from_json(input_file: str = "tasks_export.json") -> List[Dict[str, Any]]:
    """
    Load tasks from JSON export file.

    Args:
        input_file: Path to JSON file containing exported tasks

    Returns:
        List of task dictionaries
    """
    with open(input_file, 'r') as f:
        tasks = json.load(f)
    print(f"Loaded {len(tasks)} tasks from {input_file}")
    return tasks


def save_transformed_tasks(tasks: List[Dict[str, Any]], output_file: str = "tasks_transformed.json"):
    """
    Save transformed tasks to JSON file.

    Args:
        tasks: List of transformed task dictionaries
        output_file: Path to output JSON file
    """
    with open(output_file, 'w') as f:
        json.dump(tasks, f, indent=2, default=str)
    print(f"Saved {len(tasks)} transformed tasks to {output_file}")


if __name__ == "__main__":
    # Load exported tasks
    tasks = load_tasks_from_json()

    # Transform tasks for PostgreSQL
    transformed_tasks = transform_tasks_batch(tasks)

    # Save transformed tasks
    if transformed_tasks:
        save_transformed_tasks(transformed_tasks)
        print(f"Transformation complete. {len(transformed_tasks)} tasks ready for import.")
    else:
        print("No tasks to transform.")
