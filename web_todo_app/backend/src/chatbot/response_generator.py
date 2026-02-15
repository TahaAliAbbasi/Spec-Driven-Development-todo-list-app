"""
Response Generator for creating conversational chatbot responses.
Generates natural, user-friendly responses based on task execution results.
"""
from typing import Dict, Any, List
import logging
from ..models.task import TaskPublic

# Configure logging
logger = logging.getLogger(__name__)


class ResponseGenerator:
    """
    Generates conversational responses for chatbot interactions.
    Converts task execution results into natural language.
    """

    def generate_response(self, execution_result: Dict[str, Any]) -> str:
        """
        Generate a conversational response based on execution result.

        Args:
            execution_result: Dictionary with execution status and data.

        Returns:
            Natural language response string.
        """
        action = execution_result.get("action")
        logger.info(f"Generating response for action: {action}, success: {execution_result.get('success')}")

        if not execution_result.get("success"):
            error_msg = execution_result.get("message", "I encountered an error. Please try again.")
            logger.warning(f"Generating error response: {error_msg}")
            return error_msg

        if action == "create":
            return self.generate_create_response(execution_result)
        elif action == "complete":
            return self.generate_complete_response(execution_result)
        elif action == "read":
            return self.generate_read_response(execution_result)
        elif action == "update":
            return self.generate_update_response(execution_result)
        elif action == "delete":
            return self.generate_delete_response(execution_result)
        else:
            return execution_result.get("message", "Done!")

    def generate_create_response(self, result: Dict[str, Any]) -> str:
        """
        Generate response for task creation.

        Args:
            result: Execution result with created task.

        Returns:
            Conversational confirmation message.
        """
        task = result.get("task")
        if not task:
            return "I've added that task to your list."

        # Vary the response for natural conversation
        templates = [
            f"I've added '{task.title}' to your task list.",
            f"Got it! I've created a task for '{task.title}'.",
            f"Done! '{task.title}' is now on your list.",
            f"Perfect! I've added '{task.title}' to your tasks.",
        ]

        # Use task ID to deterministically select a template
        template_index = task.id % len(templates)
        return templates[template_index]

    def generate_complete_response(self, result: Dict[str, Any]) -> str:
        """
        Generate response for task completion.

        Args:
            result: Execution result with completed task.

        Returns:
            Conversational confirmation message.
        """
        task = result.get("task")
        if not task:
            return "I've marked that task as complete."

        templates = [
            f"Great! I've marked '{task.title}' as complete.",
            f"Done! '{task.title}' is now marked as complete.",
            f"Awesome! I've completed '{task.title}' for you.",
            f"Perfect! '{task.title}' is checked off your list.",
        ]

        template_index = task.id % len(templates)
        return templates[template_index]

    def generate_read_response(self, result: Dict[str, Any]) -> str:
        """
        Generate response for task querying.

        Args:
            result: Execution result with task list.

        Returns:
            Formatted task list or empty message.
        """
        tasks: List[TaskPublic] = result.get("tasks", [])
        count = result.get("count", 0)

        if count == 0:
            return "You don't have any tasks yet. Would you like to create one?"

        # Format task list
        response_lines = [f"You have {count} task{'s' if count != 1 else ''}:\n"]

        for i, task in enumerate(tasks, 1):
            status = "✓" if task.is_completed else "○"
            response_lines.append(f"{i}. {status} {task.title}")

        return "\n".join(response_lines)

    def generate_update_response(self, result: Dict[str, Any]) -> str:
        """
        Generate response for task updates.

        Args:
            result: Execution result with updated task.

        Returns:
            Conversational confirmation message.
        """
        task = result.get("task")
        if not task:
            return "I've updated that task."

        return f"I've updated the task to '{task.title}'."

    def generate_delete_response(self, result: Dict[str, Any]) -> str:
        """
        Generate response for task deletion.

        Args:
            result: Execution result with deleted task info.

        Returns:
            Conversational confirmation message.
        """
        task_title = result.get("task_title", "that task")
        return f"I've deleted '{task_title}' from your task list."

    def generate_clarification_question(self, intent) -> str:
        """
        Generate a clarification question for ambiguous intents.

        Args:
            intent: Intent object with clarification_needed field.

        Returns:
            Clarification question string.
        """
        if intent.clarification_needed:
            return intent.clarification_needed

        return "I'm not quite sure what you want to do. Could you rephrase that?"

    def generate_error_response(self, error_message: str) -> str:
        """
        Generate a user-friendly error response.

        Args:
            error_message: Technical error message.

        Returns:
            User-friendly error message.
        """
        # Map common errors to friendly messages
        error_mappings = {
            "not found": "I couldn't find that task. Could you try describing it differently?",
            "multiple": "I found multiple tasks matching that. Could you be more specific?",
            "empty": "I need more information. What would you like me to do?",
        }

        error_lower = error_message.lower()
        for key, friendly_msg in error_mappings.items():
            if key in error_lower:
                return friendly_msg

        return "I encountered an issue. Please try again or rephrase your request."


# Global response generator instance
response_generator = ResponseGenerator()
