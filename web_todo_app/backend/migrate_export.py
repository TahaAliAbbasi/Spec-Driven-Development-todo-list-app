"""
Data migration utility for moving tasks from SQLite to NeonDB (PostgreSQL).

This script provides utilities to export, transform, and migrate task data
from the existing SQLite database to the new NeonDB PostgreSQL database.
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
import os


def export_tasks_from_sqlite(sqlite_db_path: str = "todo_app.db") -> List[Dict[str, Any]]:
    """
    Export all tasks from SQLite database to a list of dictionaries.

    Args:
        sqlite_db_path: Path to the SQLite database file

    Returns:
        List of task dictionaries with all fields
    """
    if not os.path.exists(sqlite_db_path):
        print(f"SQLite database not found at {sqlite_db_path}")
        return []

    conn = sqlite3.connect(sqlite_db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM task")
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task = {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "is_completed": bool(row["is_completed"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            tasks.append(task)

        print(f"Exported {len(tasks)} tasks from SQLite database")
        return tasks

    except sqlite3.Error as e:
        print(f"Error exporting tasks from SQLite: {e}")
        return []
    finally:
        conn.close()


def save_tasks_to_json(tasks: List[Dict[str, Any]], output_file: str = "tasks_export.json"):
    """
    Save exported tasks to a JSON file for backup/inspection.

    Args:
        tasks: List of task dictionaries
        output_file: Path to output JSON file
    """
    with open(output_file, 'w') as f:
        json.dump(tasks, f, indent=2, default=str)
    print(f"Saved {len(tasks)} tasks to {output_file}")


if __name__ == "__main__":
    # Export tasks from SQLite
    tasks = export_tasks_from_sqlite()

    # Save to JSON for backup
    if tasks:
        save_tasks_to_json(tasks)
        print(f"Export complete. {len(tasks)} tasks exported.")
    else:
        print("No tasks to export.")
