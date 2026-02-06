from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base model for Task with common fields."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task model for database storage."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class TaskPublic(TaskBase):
    """Public Task model without database-specific fields."""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Model for creating new tasks."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskUpdate(SQLModel):
    """Model for updating existing tasks."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None