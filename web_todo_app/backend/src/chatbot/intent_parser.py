"""
Intent Parser for natural language understanding.
Uses OpenAI API to parse user messages and extract structured intents.
"""
from typing import Optional
import json
import logging
from openai import OpenAI
from .models import Intent, IntentAction
from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)


class IntentParser:
    """
    Parses natural language messages to identify user intent and extract parameters.
    Uses OpenAI's API for natural language understanding.
    """

    def __init__(self):
        """Initialize the intent parser with OpenAI/OpenRouter client."""
        if not settings.openai_configured:
            raise ValueError("API key not configured. Please set OPENAI_API_KEY or OPENROUTER_API_KEY in .env file.")

        # Initialize OpenAI client with OpenRouter support
        client_kwargs = {"api_key": settings.api_key}

        # Use custom base URL if provided (for OpenRouter)
        if settings.OPENAI_BASE_URL:
            client_kwargs["base_url"] = settings.OPENAI_BASE_URL

        self.client = OpenAI(**client_kwargs)
        self.model = settings.OPENAI_MODEL
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt for intent classification."""
        return """You are a task management assistant that parses user messages to identify their intent.

Your job is to analyze the user's message and return a JSON object with the following structure:
{
  "action": "CREATE" | "READ" | "UPDATE" | "DELETE" | "COMPLETE",
  "confidence": 0.0 to 1.0,
  "task_title": "extracted task title" or null,
  "task_description": "extracted description" or null,
  "ambiguous": true or false,
  "clarification_needed": "question to ask user" or null
}

INTENT DETECTION RULES:

CREATE action - User wants to add a new task:
- Phrases: "add", "create", "new task", "remind me to", "I need to", "make a task"
- Extract task_title from the message (the main thing they want to do)
- Examples:
  * "add a task to buy groceries" → task_title: "buy groceries"
  * "create a task: finish the report" → task_title: "finish the report"
  * "remind me to call mom" → task_title: "call mom"

COMPLETE action - User wants to mark a task as done:
- Phrases: "mark as done", "complete", "finished", "done with", "I finished"
- Extract task_title to identify which task
- Examples:
  * "mark buy groceries as done" → task_title: "buy groceries"
  * "I finished the report" → task_title: "the report"

READ action - User wants to see their tasks:
- Phrases: "show", "list", "what tasks", "do I have", "my tasks"
- Examples:
  * "what tasks do I have?" → no task_title needed
  * "show me incomplete tasks" → query for incomplete only

UPDATE action - User wants to modify a task:
- Phrases: "change", "update", "modify", "edit"
- Extract old task identifier and new details
- Examples:
  * "change buy milk to buy almond milk" → identify task and new title

DELETE action - User wants to remove a task:
- Phrases: "delete", "remove", "get rid of"
- Extract task_title to identify which task
- Examples:
  * "delete the groceries task" → task_title: "groceries"

CONFIDENCE SCORING:
- High confidence (0.8-1.0): Clear intent, specific task mentioned
- Medium confidence (0.5-0.7): Intent clear but task details vague
- Low confidence (0.0-0.4): Ambiguous or unclear intent

AMBIGUITY HANDLING:
- Set ambiguous=true if confidence < 0.7 OR if critical information is missing
- Provide clarification_needed with a specific question

Return ONLY valid JSON, no additional text."""

    async def parse_intent(self, message: str, context: Optional[list] = None) -> Intent:
        """
        Parse a user message to extract intent and parameters.

        Args:
            message: The user's natural language message.
            context: Optional conversation context (list of previous messages).

        Returns:
            Intent object with parsed information.
        """
        logger.info(f"Parsing intent for message: {message[:100]}...")
        try:
            # Build messages for OpenAI API
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ]

            # Call OpenAI/OpenRouter API
            logger.debug(f"Calling {self.model} API for intent parsing")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent parsing
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            # Parse the response
            content = response.choices[0].message.content
            parsed = json.loads(content)
            logger.debug(f"Parsed intent: {parsed}")

            # Create Intent object
            intent = Intent(
                action=IntentAction(parsed.get("action", "READ")),
                confidence=float(parsed.get("confidence", 0.5)),
                task_title=parsed.get("task_title"),
                task_description=parsed.get("task_description"),
                ambiguous=parsed.get("ambiguous", False),
                clarification_needed=parsed.get("clarification_needed")
            )

            # Apply confidence threshold
            if intent.confidence < settings.CHATBOT_INTENT_CONFIDENCE_THRESHOLD:
                intent.ambiguous = True
                if not intent.clarification_needed:
                    intent.clarification_needed = "I'm not quite sure what you want to do. Could you rephrase that?"
                logger.warning(f"Low confidence intent ({intent.confidence}), marked as ambiguous")

            logger.info(f"Intent parsed successfully: action={intent.action}, confidence={intent.confidence}")
            return intent

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error while parsing intent: {e}")
            # Fallback for invalid JSON
            return Intent(
                action=IntentAction.READ,
                confidence=0.0,
                ambiguous=True,
                clarification_needed="I had trouble understanding that. Could you try rephrasing?"
            )
        except Exception as e:
            logger.error(f"Error parsing intent: {e}", exc_info=True)
            # Generic error handling
            return Intent(
                action=IntentAction.READ,
                confidence=0.0,
                ambiguous=True,
                clarification_needed=f"I encountered an error: {str(e)}. Please try again."
            )


# Global intent parser instance
intent_parser = IntentParser()
