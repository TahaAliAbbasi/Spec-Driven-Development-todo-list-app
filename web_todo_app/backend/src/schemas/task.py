from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base model for Task with common fields."""
    title: str
    description: Optional[str] = None
    is_completed: bool = False


class TaskCreate(TaskBase):
    """Model for creating new tasks."""
    title: str


class TaskUpdate(BaseModel):
    """Model for updating existing tasks."""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Model for task responses."""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskToggleResponse(BaseModel):
    """Model for task toggle status response."""
    id: int
    is_completed: bool
    updated_at: datetime