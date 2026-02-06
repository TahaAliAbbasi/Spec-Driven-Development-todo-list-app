from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime

from src.database import get_session
from src.services.task_service import TaskService
from src.models.task import TaskCreate as ModelTaskCreate, TaskUpdate as ModelTaskUpdate, TaskPublic as ModelTaskPublic
from src.schemas.task import TaskResponse, TaskCreate as SchemaTaskCreate, TaskUpdate as SchemaTaskUpdate
from sqlmodel import Session


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    """Dependency to get TaskService instance."""
    return TaskService(session)

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(task_service: TaskService = Depends(get_task_service)):
    """Retrieve all tasks for the user."""
    tasks = task_service.get_all_tasks()
    # Convert from SQLModel to Pydantic response model
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_create: SchemaTaskCreate, task_service: TaskService = Depends(get_task_service)):
    """Create a new task."""
    # Validate title is not empty
    if not task_create.title or not task_create.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    # Create task using service
    task_data = ModelTaskCreate(
        title=task_create.title.strip(),
        description=task_create.description,
        is_completed=False  # New tasks are not completed by default
    )

    task = task_service.create_task(task_data)

    # Convert to response model
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    """Retrieve a specific task by ID."""
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: SchemaTaskUpdate, task_service: TaskService = Depends(get_task_service)):
    """Update an existing task."""
    # Check if task exists first
    existing_task = task_service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validate title if provided
    if task_update.title is not None:
        if not task_update.title or not task_update.title.strip():
            raise HTTPException(status_code=400, detail="Task title cannot be empty")
        task_update.title = task_update.title.strip()

    # Update task using service - convert schema to model format
    update_data = {}
    if task_update.title is not None:
        update_data['title'] = task_update.title
    if task_update.description is not None:
        update_data['description'] = task_update.description
    if task_update.is_completed is not None:
        update_data['is_completed'] = task_update.is_completed

    updated_task = task_service.update_task(task_id, ModelTaskUpdate(**update_data))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        is_completed=updated_task.is_completed,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.patch("/tasks/{task_id}/toggle-status", response_model=TaskResponse)
def toggle_task_status(task_id: int, task_service: TaskService = Depends(get_task_service)):
    """Toggle the completion status of a task."""
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    toggled_task = task_service.toggle_task_status(task_id)
    if not toggled_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=toggled_task.id,
        title=toggled_task.title,
        description=toggled_task.description,
        is_completed=toggled_task.is_completed,
        created_at=toggled_task.created_at,
        updated_at=toggled_task.updated_at
    )


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    """Delete a specific task by ID."""
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return  # Return nothing for 204 status code