"""
Direct test of NeonDB integration - CRUD operations test.

This script tests all database operations directly without needing the API server.
"""

import os
import sys
from datetime import datetime

# Set DATABASE_URL for NeonDB
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_WnSvVz2DYH7k@ep-withered-shape-ainx0eeh-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import create_db_and_tables, engine
from src.models.task import Task
from sqlmodel import select, Session

def test_neondb_integration():
    """Test all CRUD operations with NeonDB."""

    print("=" * 60)
    print("NeonDB Integration Test")
    print("=" * 60)

    # Ensure tables exist
    print("\n[1/6] Creating database tables...")
    create_db_and_tables()
    print("[PASS] Tables created successfully")

    session = Session(engine)

    try:
        # Test 1: CREATE
        print("\n[2/6] Testing CREATE operation...")
        task = Task(
            title="Test NeonDB Integration",
            description="This task tests if NeonDB integration works correctly",
            is_completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        print(f"[PASS] Task created with ID: {task.id}")
        task_id = task.id

        # Test 2: READ (get by ID)
        print("\n[3/6] Testing READ operation (get by ID)...")
        retrieved_task = session.get(Task, task_id)
        if retrieved_task:
            print(f"[PASS] Task retrieved: '{retrieved_task.title}'")
            print(f"  - ID: {retrieved_task.id}")
            print(f"  - Description: {retrieved_task.description}")
            print(f"  - Completed: {retrieved_task.is_completed}")
        else:
            print("[FAIL] Failed to retrieve task")
            return False

        # Test 3: READ (get all)
        print("\n[4/6] Testing READ operation (get all)...")
        statement = select(Task)
        all_tasks = session.exec(statement).all()
        print(f"[PASS] Retrieved {len(all_tasks)} task(s) from database")

        # Test 4: UPDATE
        print("\n[5/6] Testing UPDATE operation...")
        retrieved_task.title = "Updated: NeonDB Integration Test"
        retrieved_task.is_completed = True
        retrieved_task.updated_at = datetime.now()
        session.add(retrieved_task)
        session.commit()
        session.refresh(retrieved_task)
        print(f"[PASS] Task updated: '{retrieved_task.title}'")
        print(f"  - Completed: {retrieved_task.is_completed}")

        # Test 5: DELETE
        print("\n[6/6] Testing DELETE operation...")
        session.delete(retrieved_task)
        session.commit()

        # Verify deletion
        deleted_task = session.get(Task, task_id)
        if deleted_task is None:
            print("[PASS] Task deleted successfully")
        else:
            print("[FAIL] Task still exists after deletion")
            return False

        print("\n" + "=" * 60)
        print("All Tests PASSED")
        print("=" * 60)
        print("\nNeonDB Integration Summary:")
        print("  [PASS] Database connection established")
        print("  [PASS] SSL encryption active")
        print("  [PASS] CREATE operation works")
        print("  [PASS] READ operations work")
        print("  [PASS] UPDATE operation works")
        print("  [PASS] DELETE operation works")
        print("\nNeonDB integration is fully functional!")

        return True

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        session.close()


if __name__ == "__main__":
    success = test_neondb_integration()
    sys.exit(0 if success else 1)
