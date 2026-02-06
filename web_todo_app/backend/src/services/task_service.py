from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskCreate as ModelTaskCreate, TaskUpdate as ModelTaskUpdate, TaskPublic as ModelTaskPublic
from datetime import datetime


class TaskService:
    """Service class for managing tasks with business logic."""

    def __init__(self, session: Session):
        """Initialize the TaskService with a database session."""
        self.session = session

    def create_task(self, task_create: ModelTaskCreate) -> ModelTaskPublic:
        """Create a new task with the given data."""
        task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task.model_validate(task_create)

        # Create task using the model fields
        task = Task(
            title=task_create.title,
            description=task_create.description,
            is_completed=task_create.is_completed
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)

    def get_task_by_id(self, task_id: int) -> Optional[ModelTaskPublic]:
        """Retrieve a task by its ID."""
        task = self.session.get(Task, task_id)
        if task:
            return ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)
        return None

    def get_all_tasks(self) -> List[ModelTaskPublic]:
        """Retrieve all tasks in the collection."""
        statement = select(Task)
        tasks = self.session.execute(statement).scalars().all()
        return [
            ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)
            for task in tasks
        ]

    def get_completed_tasks(self) -> List[ModelTaskPublic]:
        """Retrieve all completed tasks."""
        statement = select(Task).where(Task.is_completed == True)
        tasks = self.session.execute(statement).scalars().all()
        return [
            ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)
            for task in tasks
        ]

    def get_incomplete_tasks(self) -> List[ModelTaskPublic]:
        """Retrieve all incomplete tasks."""
        statement = select(Task).where(Task.is_completed == False)
        tasks = self.session.execute(statement).scalars().all()
        return [
            ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)
            for task in tasks
        ]

    def update_task(self, task_id: int, task_update: ModelTaskUpdate) -> Optional[ModelTaskPublic]:
        """Update an existing task's attributes."""
        task = self.session.get(Task, task_id)
        if not task:
            return None

        # Update only the fields that are provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.now()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)

    def toggle_task_status(self, task_id: int) -> Optional[ModelTaskPublic]:
        """Toggle the completion status of a task."""
        task = self.session.get(Task, task_id)
        if not task:
            return None

        task.is_completed = not task.is_completed
        task.updated_at = datetime.now()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return ModelTaskPublic.from_orm(task) if hasattr(ModelTaskPublic, 'from_orm') else ModelTaskPublic.model_validate(task)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        task = self.session.get(Task, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True