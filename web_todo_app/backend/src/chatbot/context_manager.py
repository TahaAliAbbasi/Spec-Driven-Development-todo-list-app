"""
Context Manager for handling chat sessions and conversation context.
Manages session lifecycle, message history, and context window.
"""
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from .models import ChatSession, ChatMessage, MessageSender
from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)


class ContextManager:
    """
    Manages chat sessions with in-memory storage.
    Handles session creation, retrieval, updates, and cleanup.
    """

    def __init__(self):
        """Initialize the context manager with empty session storage."""
        self._sessions: Dict[str, ChatSession] = {}

    def create_session(self, session_id: Optional[str] = None) -> ChatSession:
        """
        Create a new chat session.

        Args:
            session_id: Optional session ID. If not provided, generates a new UUID.

        Returns:
            ChatSession: The newly created session.
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        now = datetime.now()
        expires_at = now + timedelta(seconds=settings.CHATBOT_SESSION_TTL)

        session = ChatSession(
            id=session_id,
            messages=[],
            context_window=[],
            created_at=now,
            last_activity=now,
            expires_at=expires_at
        )

        self._sessions[session_id] = session
        logger.info(f"Created new chat session: {session_id}, expires at {expires_at}")
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Retrieve a session by ID.

        Args:
            session_id: The session ID to retrieve.

        Returns:
            ChatSession if found and not expired, None otherwise.
        """
        session = self._sessions.get(session_id)

        if session is None:
            logger.warning(f"Session not found: {session_id}")
            return None

        # Check if session has expired
        if datetime.now() > session.expires_at:
            # Clean up expired session
            logger.info(f"Session expired, removing: {session_id}")
            del self._sessions[session_id]
            return None

        logger.debug(f"Retrieved session: {session_id}, messages: {len(session.messages)}")
        return session

    def update_session(
        self,
        session_id: str,
        user_message: ChatMessage,
        bot_message: ChatMessage
    ) -> Optional[ChatSession]:
        """
        Update a session with new messages.

        Args:
            session_id: The session ID to update.
            user_message: The user's message to add.
            bot_message: The bot's response message to add.

        Returns:
            Updated ChatSession if found, None otherwise.
        """
        session = self.get_session(session_id)

        if session is None:
            return None

        # Add messages to history
        session.messages.append(user_message)
        session.messages.append(bot_message)

        # Maintain max 50 messages (FIFO eviction)
        if len(session.messages) > 50:
            session.messages = session.messages[-50:]

        # Update context window (last 10 messages)
        self._update_context_window(session)

        # Update session metadata
        now = datetime.now()
        session.last_activity = now
        session.expires_at = now + timedelta(seconds=settings.CHATBOT_SESSION_TTL)

        self._sessions[session_id] = session
        return session

    def _update_context_window(self, session: ChatSession) -> None:
        """
        Update the context window with the most recent messages.

        Args:
            session: The session to update.
        """
        max_context = settings.CHATBOT_MAX_CONTEXT_MESSAGES
        session.context_window = session.messages[-max_context:] if len(session.messages) > max_context else session.messages.copy()

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session by ID.

        Args:
            session_id: The session ID to delete.

        Returns:
            True if session was deleted, False if not found.
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions from storage.

        Returns:
            Number of sessions cleaned up.
        """
        now = datetime.now()
        expired_ids = [
            session_id
            for session_id, session in self._sessions.items()
            if now > session.expires_at
        ]

        for session_id in expired_ids:
            del self._sessions[session_id]

        return len(expired_ids)

    def get_session_count(self) -> int:
        """
        Get the total number of active sessions.

        Returns:
            Number of active sessions.
        """
        return len(self._sessions)


# Global context manager instance
context_manager = ContextManager()
