"""
Data integrity verification utility for migration validation.

This script verifies that data migrated from SQLite to NeonDB maintains
integrity and completeness.
"""

import os
import sys
from typing import List, Dict, Any, Tuple
from sqlmodel import Session, create_engine, select

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.models.task import Task
from migrate_export import export_tasks_from_sqlite


def verify_task_count(sqlite_tasks: List[Dict[str, Any]], neondb_url: str) -> Tuple[bool, str]:
    """
    Verify that the number of tasks matches between SQLite and NeonDB.

    Args:
        sqlite_tasks: List of tasks from SQLite export
        neondb_url: PostgreSQL connection string for NeonDB

    Returns:
        Tuple of (success, message)
    """
    engine = create_engine(neondb_url, echo=False)

    with Session(engine) as session:
        statement = select(Task)
        neondb_tasks = session.exec(statement).all()

        sqlite_count = len(sqlite_tasks)
        neondb_count = len(neondb_tasks)

        if sqlite_count == neondb_count:
            return True, f"✓ Task count matches: {sqlite_count} tasks in both databases"
        else:
            return False, f"✗ Task count mismatch: SQLite has {sqlite_count}, NeonDB has {neondb_count}"


def verify_task_data(sqlite_tasks: List[Dict[str, Any]], neondb_url: str) -> Tuple[bool, List[str]]:
    """
    Verify that task data matches between SQLite and NeonDB.

    Args:
        sqlite_tasks: List of tasks from SQLite export
        neondb_url: PostgreSQL connection string for NeonDB

    Returns:
        Tuple of (success, list of error messages)
    """
    engine = create_engine(neondb_url, echo=False)
    errors = []

    with Session(engine) as session:
        # Create a mapping of SQLite tasks by title (since IDs may differ)
        sqlite_by_title = {task["title"]: task for task in sqlite_tasks}

        statement = select(Task)
        neondb_tasks = session.exec(statement).all()

        # Check each NeonDB task against SQLite data
        for neondb_task in neondb_tasks:
            sqlite_task = sqlite_by_title.get(neondb_task.title)

            if not sqlite_task:
                errors.append(f"Task '{neondb_task.title}' exists in NeonDB but not in SQLite")
                continue

            # Verify field values
            if neondb_task.description != sqlite_task["description"]:
                errors.append(f"Description mismatch for task '{neondb_task.title}'")

            if neondb_task.is_completed != bool(sqlite_task["is_completed"]):
                errors.append(f"Completion status mismatch for task '{neondb_task.title}'")

        # Check for tasks in SQLite that are missing in NeonDB
        neondb_titles = {task.title for task in neondb_tasks}
        for sqlite_task in sqlite_tasks:
            if sqlite_task["title"] not in neondb_titles:
                errors.append(f"Task '{sqlite_task['title']}' exists in SQLite but not in NeonDB")

    success = len(errors) == 0
    return success, errors


def run_verification(sqlite_db_path: str = "todo_app.db", neondb_url: str = None) -> bool:
    """
    Run complete data integrity verification.

    Args:
        sqlite_db_path: Path to SQLite database file
        neondb_url: PostgreSQL connection string for NeonDB

    Returns:
        True if verification passes, False otherwise
    """
    print("=" * 60)
    print("Data Integrity Verification")
    print("=" * 60)

    # Get NeonDB URL from environment if not provided
    if not neondb_url:
        neondb_url = os.getenv("DATABASE_URL")
        if not neondb_url or neondb_url.startswith("sqlite"):
            print("ERROR: DATABASE_URL must be set to NeonDB PostgreSQL connection string")
            return False

    # Export SQLite data for comparison
    print("\n[1/3] Exporting SQLite data for comparison...")
    sqlite_tasks = export_tasks_from_sqlite(sqlite_db_path)
    if not sqlite_tasks:
        print("No tasks in SQLite database to verify")
        return True

    # Verify task count
    print("\n[2/3] Verifying task count...")
    count_success, count_message = verify_task_count(sqlite_tasks, neondb_url)
    print(count_message)

    # Verify task data
    print("\n[3/3] Verifying task data integrity...")
    data_success, data_errors = verify_task_data(sqlite_tasks, neondb_url)

    if data_success:
        print("✓ All task data verified successfully")
    else:
        print(f"✗ Found {len(data_errors)} data integrity issues:")
        for error in data_errors:
            print(f"  - {error}")

    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    overall_success = count_success and data_success

    if overall_success:
        print("✓ Data integrity verification PASSED")
        print("All tasks migrated successfully with no data loss")
    else:
        print("✗ Data integrity verification FAILED")
        print("Please review errors above and re-run migration if needed")

    print("=" * 60)

    return overall_success


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
