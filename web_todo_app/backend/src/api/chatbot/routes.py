"""
FastAPI router for chatbot endpoints.
Handles chat message processing, session management, and conversation flow.
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import Optional
import uuid

from .schemas import MessageRequest, MessageResponse, SessionResponse, ErrorResponse
from ...chatbot.context_manager import context_manager
from ...chatbot.models import ChatMessage, MessageSender
from ...config import settings

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])


@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    Process a user message, parse intent, execute task operations, and return a conversational response.

    This is the primary endpoint for chatbot interaction. It handles:
    - Natural language understanding via intent parsing
    - Task operations (CREATE, READ, UPDATE, DELETE, COMPLETE)
    - Session management and conversation context
    - Ambiguity detection and clarification requests

    Args:
        request: MessageRequest containing the user's message and optional session_id

    Returns:
        MessageResponse with the bot's response, parsed intent, and session information

    Raises:
        HTTPException 400: If message content is empty
        HTTPException 404: If provided session_id is not found or expired
        HTTPException 500: If an unexpected error occurs during processing

    Example:
        ```json
        POST /api/chatbot/message
        {
            "message": "add a task to buy groceries",
            "session_id": "optional-session-id"
        }
        ```
    """
    try:
        # Validate message content
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )

        # Get or create session
        session_id = request.session_id
        if session_id:
            session = context_manager.get_session(session_id)
            if session is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Session not found or expired. Please start a new conversation."
                )
        else:
            session = context_manager.create_session()
            session_id = session.id

        # Create user message
        user_message_id = str(uuid.uuid4())
        now = datetime.now()

        # Import chatbot components
        from ...chatbot.intent_parser import intent_parser
        from ...chatbot.task_executor import TaskExecutor
        from ...chatbot.response_generator import response_generator
        from ...database import get_session as get_db_session

        # Parse intent from user message
        intent = await intent_parser.parse_intent(request.message, session.context_window)

        # Check if intent is ambiguous
        if intent.ambiguous:
            bot_response = response_generator.generate_clarification_question(intent)
            bot_message_id = str(uuid.uuid4())

            user_message = ChatMessage(
                id=user_message_id,
                session_id=session_id,
                sender=MessageSender.USER,
                content=request.message,
                timestamp=now
            )

            bot_message = ChatMessage(
                id=bot_message_id,
                session_id=session_id,
                sender=MessageSender.BOT,
                content=bot_response,
                timestamp=now,
                intent=intent
            )

            context_manager.update_session(session_id, user_message, bot_message)

            return MessageResponse(
                message_id=bot_message_id,
                session_id=session_id,
                response=bot_response,
                intent=intent,
                timestamp=now
            )

        # Execute task operation
        db_session = next(get_db_session())
        try:
            task_executor = TaskExecutor(db_session)
            execution_result = await task_executor.execute(intent)

            # Generate conversational response
            if execution_result.get("success"):
                bot_response = response_generator.generate_response(execution_result)
            else:
                bot_response = execution_result.get("message", "I couldn't complete that action.")

            # Create bot message
            bot_message_id = str(uuid.uuid4())

            user_message = ChatMessage(
                id=user_message_id,
                session_id=session_id,
                sender=MessageSender.USER,
                content=request.message,
                timestamp=now
            )

            bot_message = ChatMessage(
                id=bot_message_id,
                session_id=session_id,
                sender=MessageSender.BOT,
                content=bot_response,
                timestamp=now,
                intent=intent
            )

            # Update session with messages
            context_manager.update_session(session_id, user_message, bot_message)

            return MessageResponse(
                message_id=bot_message_id,
                session_id=session_id,
                response=bot_response,
                intent=intent,
                timestamp=now
            )
        finally:
            db_session.close()

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/session", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Retrieve session metadata and message history for the current conversation.

    This endpoint allows clients to fetch the complete conversation history
    and session information, including message count, timestamps, and expiry.

    Args:
        session_id: Unique identifier for the chat session

    Returns:
        SessionResponse with session metadata and full message history

    Raises:
        HTTPException 404: If session is not found or has expired

    Example:
        ```
        GET /api/chatbot/session?session_id=abc-123-def
        ```
    """
    session = context_manager.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or expired"
        )

    return SessionResponse(
        session_id=session.id,
        message_count=len(session.messages),
        created_at=session.created_at,
        last_activity=session.last_activity,
        expires_at=session.expires_at,
        messages=session.messages
    )


@router.delete("/session", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    """
    Delete the session and all associated messages.

    This endpoint permanently removes a chat session and its entire conversation history.
    The user will need to start a new conversation after deletion.

    Args:
        session_id: Unique identifier for the chat session to delete

    Returns:
        None (204 No Content on success)

    Raises:
        HTTPException 404: If session is not found

    Example:
        ```
        DELETE /api/chatbot/session?session_id=abc-123-def
        ```
    """
    deleted = context_manager.delete_session(session_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    return None
