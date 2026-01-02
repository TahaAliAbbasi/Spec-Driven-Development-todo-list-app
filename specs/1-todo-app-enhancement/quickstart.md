# Quickstart Guide: Todo App CLI Enhancement

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Setup
1. Navigate to the project directory containing the todo app
2. Install required dependencies (if any):
   ```bash
   pip install colorama  # for colored text support
   ```

## Running the Enhanced Todo App
1. Execute the main application file:
   ```bash
   python todo_app/todo_app.py
   ```

## Available Commands
- `add "task description"` - Add a new task (marked incomplete by default)
- `complete <task_id>` - Mark a task as completed (shows ✓)
- `incomplete <task_id>` - Mark a task as incomplete (shows ✗)
- `edit <task_id> "new task description"` - Edit an existing task
- `list` - Display all tasks with emoji indicators and styled text
- `delete <task_id>` - Remove a task from the list
- `quit` or `exit` - Exit the application

## Example Usage
```
> add "Buy groceries"
Added task: Buy groceries [ID: 1, Status: ✗]

> add "Finish report"
Added task: Finish report [ID: 2, Status: ✗]

> complete 1
Task 1 marked as completed: ✓ Buy groceries

> list
TODO LIST:
1. ✓ Buy groceries
2. ✗ Finish report

> edit 2 "Finish quarterly report"
Task 2 updated: ✗ Finish quarterly report

> list
TODO LIST:
1. ✓ Buy groceries
2. ✗ Finish quarterly report
```

## Key Enhancements
- Tasks display with checkmark (✓) for completed and cross (✗) for incomplete
- New tasks are automatically marked as incomplete
- Text styling with colors and bold headings
- Ability to edit existing tasks from CLI