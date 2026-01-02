# Data Model: Todo App CLI Enhancement

## Task Entity

**Name**: Task
**Description**: Represents a todo item with text content, completion status, and display formatting

**Fields**:
- `id` (int): Unique identifier for the task
- `text` (str): The task description text
- `completed` (bool): Status indicating if the task is completed (default: False)
- `created_at` (datetime): Timestamp when the task was created

**Validation Rules**:
- `id` must be unique within the task list
- `text` must not be empty or None
- `completed` defaults to False when creating new tasks

**State Transitions**:
- New Task: `completed = False` (default)
- Complete Task: `completed = True`
- Incomplete Task: `completed = False`

## TaskList Entity

**Name**: TaskList
**Description**: Collection of tasks with operations for managing the list

**Fields**:
- `tasks` (List[Task]): Collection of Task objects
- `next_id` (int): Counter for generating unique task IDs

**Operations**:
- `add_task(text: str)`: Creates a new task with `completed = False`
- `complete_task(id: int)`: Sets task's `completed` status to True
- `incomplete_task(id: int)`: Sets task's `completed` status to False
- `edit_task(id: int, new_text: str)`: Updates the text of an existing task
- `delete_task(id: int)`: Removes a task from the list
- `get_task(id: int)`: Retrieves a specific task by ID
- `get_all_tasks()`: Returns all tasks in the list
- `display_tasks()`: Returns formatted string representation with emojis and styling