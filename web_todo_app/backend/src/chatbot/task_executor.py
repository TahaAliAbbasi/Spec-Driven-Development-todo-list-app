"""
Task Executor for performing task operations.
Executes CRUD operations on tasks based on parsed intents.
"""
from typing import Optional, List
import logging
from sqlmodel import Session
from .models import Intent, IntentAction
from ..services.task_service import TaskService
from ..schemas.task import TaskCreate, TaskUpdate
from ..models.task import TaskPublic
from ..database import get_session

# Configure logging
logger = logging.getLogger(__name__)


class TaskExecutor:
    """
    Executes task operations based on parsed intents.
    Integrates with existing TaskService to perform CRUD operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the task executor with a database session.

        Args:
            session: SQLModel database session.
        """
        self.task_service = TaskService(session)

    async def execute(self, intent: Intent) -> dict:
        """
        Execute a task operation based on the intent.

        Args:
            intent: Parsed intent with action and parameters.

        Returns:
            Dictionary with execution result and metadata.
        """
        logger.info(f"Executing task operation: action={intent.action}, task_title={intent.task_title}")
        try:
            if intent.action == IntentAction.CREATE:
                return await self.execute_create(intent)
            elif intent.action == IntentAction.COMPLETE:
                return await self.execute_complete(intent)
            elif intent.action == IntentAction.READ:
                return await self.execute_read(intent)
            elif intent.action == IntentAction.UPDATE:
                return await self.execute_update(intent)
            elif intent.action == IntentAction.DELETE:
                return await self.execute_delete(intent)
            else:
                logger.warning(f"Unknown action attempted: {intent.action}")
                return {
                    "success": False,
                    "error": "Unknown action",
                    "message": "I don't know how to handle that action."
                }
        except Exception as e:
            logger.error(f"Error executing task operation: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "message": f"An error occurred: {str(e)}"
            }

    async def execute_create(self, intent: Intent) -> dict:
        """
        Create a new task.

        Args:
            intent: Intent with task_title and optional task_description.

        Returns:
            Dictionary with created task and success status.
        """
        if not intent.task_title:
            return {
                "success": False,
                "error": "Missing task title",
                "message": "I need to know what task you want to create."
            }

        try:
            task_create = TaskCreate(
                title=intent.task_title,
                description=intent.task_description,
                is_completed=False
            )

            created_task = self.task_service.create_task(task_create)

            return {
                "success": True,
                "action": "create",
                "task": created_task,
                "message": f"I've added '{created_task.title}' to your task list."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I couldn't create that task. Please try again."
            }

    async def execute_complete(self, intent: Intent) -> dict:
        """
        Mark a task as complete.

        Args:
            intent: Intent with task_id or task_title to identify the task.

        Returns:
            Dictionary with updated task and success status.
        """
        # Find the task
        task = await self._find_task(intent)

        if task is None:
            return {
                "success": False,
                "error": "Task not found",
                "message": "I couldn't find a task matching that description. Could you be more specific?"
            }

        if isinstance(task, list):
            # Multiple tasks found
            task_list = "\n".join([f"- {t.title}" for t in task[:5]])
            return {
                "success": False,
                "error": "Multiple tasks found",
                "message": f"I found multiple tasks. Which one did you mean?\n{task_list}",
                "tasks": task
            }

        try:
            # Toggle task status (mark as complete)
            updated_task = self.task_service.toggle_task_status(task.id)

            if updated_task and updated_task.is_completed:
                return {
                    "success": True,
                    "action": "complete",
                    "task": updated_task,
                    "message": f"Great! I've marked '{updated_task.title}' as complete."
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to complete task",
                    "message": "I couldn't mark that task as complete. Please try again."
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an error while completing that task."
            }

    async def execute_read(self, intent: Intent) -> dict:
        """
        Query and retrieve tasks.

        Args:
            intent: Intent with optional query_filter.

        Returns:
            Dictionary with task list and success status.
        """
        try:
            # Determine which tasks to retrieve
            query_filter = intent.query_filter or {}

            if query_filter.get("is_completed") == False:
                tasks = self.task_service.get_incomplete_tasks()
            elif query_filter.get("is_completed") == True:
                tasks = self.task_service.get_completed_tasks()
            elif query_filter.get("search_term"):
                # Search by title
                all_tasks = self.task_service.get_all_tasks()
                search_term = query_filter["search_term"].lower()
                tasks = [t for t in all_tasks if search_term in t.title.lower()]
            else:
                tasks = self.task_service.get_all_tasks()

            return {
                "success": True,
                "action": "read",
                "tasks": tasks,
                "count": len(tasks),
                "message": f"I found {len(tasks)} task{'s' if len(tasks) != 1 else ''}."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I couldn't retrieve your tasks. Please try again."
            }

    async def execute_update(self, intent: Intent) -> dict:
        """
        Update an existing task.

        Args:
            intent: Intent with task identifier and new details.

        Returns:
            Dictionary with updated task and success status.
        """
        # Find the task
        task = await self._find_task(intent)

        if task is None:
            return {
                "success": False,
                "error": "Task not found",
                "message": "I couldn't find a task matching that description."
            }

        if isinstance(task, list):
            task_list = "\n".join([f"- {t.title}" for t in task[:5]])
            return {
                "success": False,
                "error": "Multiple tasks found",
                "message": f"I found multiple tasks. Which one did you mean?\n{task_list}",
                "tasks": task
            }

        try:
            task_update = TaskUpdate(
                title=intent.task_title,
                description=intent.task_description
            )

            updated_task = self.task_service.update_task(task.id, task_update)

            if updated_task:
                return {
                    "success": True,
                    "action": "update",
                    "task": updated_task,
                    "message": f"I've updated the task to '{updated_task.title}'."
                }
            else:
                return {
                    "success": False,
                    "error": "Update failed",
                    "message": "I couldn't update that task."
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an error while updating that task."
            }

    async def execute_delete(self, intent: Intent) -> dict:
        """
        Delete a task.

        Args:
            intent: Intent with task identifier.

        Returns:
            Dictionary with success status.
        """
        # Find the task
        task = await self._find_task(intent)

        if task is None:
            return {
                "success": False,
                "error": "Task not found",
                "message": "I couldn't find a task matching that description."
            }

        if isinstance(task, list):
            task_list = "\n".join([f"- {t.title}" for t in task[:5]])
            return {
                "success": False,
                "error": "Multiple tasks found",
                "message": f"I found multiple tasks. Which one did you mean?\n{task_list}",
                "tasks": task
            }

        try:
            deleted = self.task_service.delete_task(task.id)

            if deleted:
                return {
                    "success": True,
                    "action": "delete",
                    "task_title": task.title,
                    "message": f"I've deleted '{task.title}' from your task list."
                }
            else:
                return {
                    "success": False,
                    "error": "Delete failed",
                    "message": "I couldn't delete that task."
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an error while deleting that task."
            }

    async def _find_task(self, intent: Intent) -> Optional[TaskPublic | List[TaskPublic]]:
        """
        Find a task by ID or title.

        Args:
            intent: Intent with task_id or task_title.

        Returns:
            Single task, list of matching tasks, or None.
        """
        # Try to find by ID first
        if intent.task_id:
            return self.task_service.get_task_by_id(intent.task_id)

        # Find by title
        if intent.task_title:
            all_tasks = self.task_service.get_all_tasks()
            search_term = intent.task_title.lower()

            # Exact match
            exact_matches = [t for t in all_tasks if t.title.lower() == search_term]
            if len(exact_matches) == 1:
                return exact_matches[0]
            elif len(exact_matches) > 1:
                return exact_matches

            # Partial match
            partial_matches = [t for t in all_tasks if search_term in t.title.lower()]
            if len(partial_matches) == 1:
                return partial_matches[0]
            elif len(partial_matches) > 1:
                return partial_matches

        return None
