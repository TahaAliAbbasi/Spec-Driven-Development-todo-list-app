"""
Pydantic models for the AI-powered chatbot feature.
Defines data structures for chat messages, sessions, and intents.
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MessageSender(str, Enum):
    """Enum for message sender types."""
    USER = "user"
    BOT = "bot"


class IntentAction(str, Enum):
    """Enum for intent action types."""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    COMPLETE = "COMPLETE"


class Intent(BaseModel):
    """Represents a parsed user intent with extracted parameters."""
    action: IntentAction
    confidence: float = Field(ge=0.0, le=1.0)
    task_id: Optional[int] = None
    task_title: Optional[str] = Field(None, min_length=1, max_length=200)
    task_description: Optional[str] = Field(None, max_length=1000)
    query_filter: Optional[Dict[str, Any]] = None
    ambiguous: bool
    clarification_needed: Optional[str] = Field(None, max_length=500)

    class Config:
        use_enum_values = True


class ChatMessage(BaseModel):
    """Represents a single message in a conversation."""
    id: str
    session_id: str
    sender: MessageSender
    content: str = Field(min_length=1, max_length=2000)
    timestamp: datetime
    intent: Optional[Intent] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True


class ChatSession(BaseModel):
    """Represents a conversation session with message history."""
    id: str
    messages: List[ChatMessage] = Field(default_factory=list, max_length=50)
    context_window: List[ChatMessage] = Field(default_factory=list, max_length=10)
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True
