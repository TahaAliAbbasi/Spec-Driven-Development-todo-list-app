"""
Main migration script to move tasks from SQLite to NeonDB (PostgreSQL).

This script orchestrates the complete migration process:
1. Export tasks from SQLite
2. Transform data for PostgreSQL compatibility
3. Import tasks into NeonDB
4. Verify data integrity
"""

import os
import sys
from typing import List, Dict, Any
from sqlmodel import Session, create_engine, select
from migrate_export import export_tasks_from_sqlite, save_tasks_to_json
from migrate_transform import transform_tasks_batch, save_transformed_tasks

# Add parent directory to path to import models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.models.task import Task


def import_tasks_to_neondb(tasks: List[Dict[str, Any]], database_url: str) -> int:
    """
    Import transformed tasks into NeonDB PostgreSQL database.

    Args:
        tasks: List of transformed task dictionaries
        database_url: PostgreSQL connection string for NeonDB

    Returns:
        Number of tasks successfully imported
    """
    if not database_url or database_url.startswith("sqlite"):
        raise ValueError("DATABASE_URL must be set to a PostgreSQL connection string")

    # Create engine for NeonDB
    engine = create_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=True  # Enable SQL logging for migration
    )

    # Create tables if they don't exist
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    imported_count = 0
    errors = []

    with Session(engine) as session:
        for task_data in tasks:
            try:
                # Create Task object without id to let PostgreSQL auto-generate
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    is_completed=task_data["is_completed"],
                    created_at=task_data["created_at"],
                    updated_at=task_data["updated_at"]
                )

                session.add(task)
                imported_count += 1

            except Exception as e:
                errors.append(f"Error importing task {task_data.get('id', 'unknown')}: {e}")

        # Commit all tasks at once
        try:
            session.commit()
            print(f"Successfully imported {imported_count} tasks to NeonDB")
        except Exception as e:
            session.rollback()
            print(f"Error committing tasks to database: {e}")
            return 0

    if errors:
        print("\nImport errors:")
        for error in errors:
            print(f"  - {error}")

    return imported_count


def run_migration(sqlite_db_path: str = "todo_app.db", neondb_url: str = None):
    """
    Run the complete migration process from SQLite to NeonDB.

    Args:
        sqlite_db_path: Path to SQLite database file
        neondb_url: PostgreSQL connection string for NeonDB
    """
    print("=" * 60)
    print("Starting migration from SQLite to NeonDB")
    print("=" * 60)

    # Get NeonDB URL from environment if not provided
    if not neondb_url:
        neondb_url = os.getenv("DATABASE_URL")
        if not neondb_url or neondb_url.startswith("sqlite"):
            print("ERROR: DATABASE_URL environment variable must be set to NeonDB PostgreSQL connection string")
            print("Example: postgresql://user:password@host/database?sslmode=require")
            return False

    # Step 1: Export from SQLite
    print("\n[1/4] Exporting tasks from SQLite...")
    tasks = export_tasks_from_sqlite(sqlite_db_path)
    if not tasks:
        print("No tasks found in SQLite database. Migration complete (nothing to migrate).")
        return True

    # Save backup
    save_tasks_to_json(tasks, "tasks_backup.json")

    # Step 2: Transform data
    print("\n[2/4] Transforming data for PostgreSQL...")
    transformed_tasks = transform_tasks_batch(tasks)
    if not transformed_tasks:
        print("ERROR: No tasks could be transformed. Migration aborted.")
        return False

    save_transformed_tasks(transformed_tasks, "tasks_ready_for_import.json")

    # Step 3: Import to NeonDB
    print("\n[3/4] Importing tasks to NeonDB...")
    imported_count = import_tasks_to_neondb(transformed_tasks, neondb_url)

    # Step 4: Summary
    print("\n[4/4] Migration Summary")
    print("=" * 60)
    print(f"Tasks in SQLite:        {len(tasks)}")
    print(f"Tasks transformed:      {len(transformed_tasks)}")
    print(f"Tasks imported:         {imported_count}")
    print(f"Success rate:           {imported_count}/{len(tasks)} ({100*imported_count/len(tasks):.1f}%)")
    print("=" * 60)

    if imported_count == len(tasks):
        print("\n✓ Migration completed successfully!")
        return True
    else:
        print(f"\n⚠ Migration completed with {len(tasks) - imported_count} errors")
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
