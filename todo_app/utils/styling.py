"""
Text styling utilities for the Console Todo Application.

This module provides functions for text styling including colored text,
bold formatting, and emoji indicators for task status.
"""

def get_emoji_status(is_completed: bool) -> str:
    """
    Get emoji indicator for task completion status.

    Args:
        is_completed: Boolean indicating if task is completed

    Returns:
        String with appropriate emoji indicator
    """
    return "✓" if is_completed else "✗"


def get_colored_text(text: str, color: str = "white") -> str:
    """
    Apply color to text using ANSI escape codes.

    Args:
        text: The text to color
        color: Color name (red, green, yellow, blue, magenta, cyan, white)

    Returns:
        String with ANSI color codes applied
    """
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    color_code = colors.get(color.lower(), colors["white"])
    reset_code = colors["reset"]

    return f"{color_code}{text}{reset_code}"


def get_bold_text(text: str) -> str:
    """
    Apply bold formatting to text using ANSI escape codes.

    Args:
        text: The text to make bold

    Returns:
        String with ANSI bold code applied
    """
    return f"\033[1m{text}\033[0m"


def get_styled_task_display(task) -> str:
    """
    Get a styled display string for a task with emoji and colors.

    Args:
        task: Task object to display

    Returns:
        Formatted string with emoji, colors, and styling
    """
    emoji = get_emoji_status(task.is_completed)
    status_color = "green" if task.is_completed else "red"
    emoji_colored = get_colored_text(emoji, status_color)

    # Style the task title based on completion status
    title_color = "green" if task.is_completed else "white"
    title_styled = get_colored_text(task.title, title_color)

    if task.description:
        return f"{emoji_colored} {title_styled} - {task.description}"
    else:
        return f"{emoji_colored} {title_styled}"


def get_heading_styled(text: str) -> str:
    """
    Get a styled heading with bold formatting.

    Args:
        text: The heading text

    Returns:
        Bold formatted heading string
    """
    return get_bold_text(text)