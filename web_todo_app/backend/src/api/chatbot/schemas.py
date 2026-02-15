"""
API request and response schemas for chatbot endpoints.
Defines Pydantic models for API communication.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from ...chatbot.models import Intent, ChatMessage


class MessageRequest(BaseModel):
    """Request schema for sending a message to the chatbot."""
    session_id: Optional[str] = Field(None, description="Session identifier. If not provided, a new session will be created.")
    message: str = Field(..., min_length=1, max_length=2000, description="User's natural language message")


class MessageResponse(BaseModel):
    """Response schema for chatbot message processing."""
    message_id: str = Field(..., description="Unique identifier for this message")
    session_id: str = Field(..., description="Session identifier")
    response: str = Field(..., description="Chatbot's conversational response")
    intent: Optional[Intent] = Field(None, description="Parsed intent from user message")
    timestamp: datetime = Field(..., description="Response timestamp")


class SessionResponse(BaseModel):
    """Response schema for session information."""
    session_id: str = Field(..., description="Unique session identifier")
    message_count: int = Field(..., description="Total number of messages in the session")
    created_at: datetime = Field(..., description="Session creation timestamp")
    last_activity: datetime = Field(..., description="Last message timestamp")
    expires_at: datetime = Field(..., description="Session expiry timestamp")
    messages: List[ChatMessage] = Field(..., description="Ordered list of messages in the conversation")


class ErrorResponse(BaseModel):
    """Response schema for error messages."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    timestamp: datetime = Field(..., description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
