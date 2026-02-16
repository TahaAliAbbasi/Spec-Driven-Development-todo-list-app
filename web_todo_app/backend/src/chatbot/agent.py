"""
AI Agent using openai-agents SDK for task management.
Uses OpenRouter API with function calling capabilities.
"""
import logging
from typing import Optional, List, Dict, Any
from agents import AsyncOpenAI, Agent, OpenAIChatCompletionsModel
from sqlmodel import Session

from ..config import settings
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)


def create_task_tool(db_session: Session):
    """Tool function to create a new task."""
    task_service = TaskService(db_session)

    def create_task(title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task in the todo list.

        Args:
            title: The title/name of the task
            description: Optional description or details about the task

        Returns:
            Dictionary with task details
        """
        try:
            task_create = TaskCreate(
                title=title,
                description=description,
                is_completed=False
            )
            task = task_service.create_task(task_create)
            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed
                }
            }
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return {"success": False, "error": str(e)}

    return create_task


def get_tasks_tool(db_session: Session):
    """Tool function to get tasks."""
    task_service = TaskService(db_session)

    def get_tasks(completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get all tasks or filter tasks by completion status.

        Args:
            completed: Filter by completion status. True for completed tasks,
                      False for incomplete tasks. Omit to get all tasks.

        Returns:
            Dictionary with list of tasks
        """
        try:
            tasks = task_service.get_tasks()

            # Filter by completion status if specified
            if completed is not None:
                tasks = [t for t in tasks if t.is_completed == completed]

            return {
                "success": True,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "is_completed": t.is_completed
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            }
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            return {"success": False, "error": str(e)}

    return get_tasks


def update_task_tool(db_session: Session):
    """Tool function to update a task."""
    task_service = TaskService(db_session)

    def update_task(
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update an existing task's title, description, or completion status.

        Args:
            task_id: The ID of the task to update
            title: New title for the task
            description: New description for the task
            is_completed: Mark task as completed (true) or incomplete (false)

        Returns:
            Dictionary with updated task details
        """
        try:
            # Build update object with only provided fields
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if is_completed is not None:
                update_data["is_completed"] = is_completed

            task_update = TaskUpdate(**update_data)
            task = task_service.update_task(task_id, task_update)

            if not task:
                return {"success": False, "error": "Task not found"}

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed
                }
            }
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return {"success": False, "error": str(e)}

    return update_task


def delete_task_tool(db_session: Session):
    """Tool function to delete a task."""
    task_service = TaskService(db_session)

    def delete_task(task_id: int) -> Dict[str, Any]:
        """
        Delete a task from the todo list.

        Args:
            task_id: The ID of the task to delete

        Returns:
            Dictionary with success status
        """
        try:
            success = task_service.delete_task(task_id)

            if not success:
                return {"success": False, "error": "Task not found"}

            return {"success": True, "task_id": task_id}
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return {"success": False, "error": str(e)}

    return delete_task


def create_task_agent(db_session: Session) -> Agent:
    """
    Create an AI agent with task management tools.

    Args:
        db_session: Database session for task operations

    Returns:
        Configured Agent instance
    """
    # Initialize OpenAI client with OpenRouter
    api_key = settings.OPENROUTER_API_KEY or settings.OPENAI_API_KEY
    base_url = settings.OPENAI_BASE_URL or "https://api.openai.com/v1"

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # Create model
    model = OpenAIChatCompletionsModel(
        model=settings.OPENAI_MODEL,
        openai_client=client
    )

    # Create agent with tools
    agent = Agent(
        name="TaskAssistant",
        model=model,
        instructions="""You are a helpful task management assistant. You can create, read, update, and delete tasks.

Be conversational and friendly. When users ask about their tasks, use the get_tasks function.
When they want to add a task, use create_task. For updates or marking complete, use update_task.
For deletions, use delete_task.

Always confirm actions in a natural, friendly way. If a user's request is ambiguous, ask for clarification.""",
        tools=[
            create_task_tool(db_session),
            get_tasks_tool(db_session),
            update_task_tool(db_session),
            delete_task_tool(db_session)
        ]
    )

    logger.info(f"TaskAgent created with model: {settings.OPENAI_MODEL}")
    return agent
