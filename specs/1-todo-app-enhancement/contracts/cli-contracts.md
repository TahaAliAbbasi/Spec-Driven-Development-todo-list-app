# Todo App CLI Contracts

## Command Interface Specification

### Add Task Command
- **Command**: `add "task description"`
- **Input**: Task description string
- **Output**: Task object with ID, text, and status (incomplete by default)
- **Success Response**: "Added task: [task text] [ID: n, Status: ✗]"
- **Error Response**: Appropriate error message if input is invalid

### Complete Task Command
- **Command**: `complete <task_id>`
- **Input**: Task ID (integer)
- **Output**: Updated task with completed status
- **Success Response**: "Task n marked as completed: ✓ [task text]"
- **Error Response**: Error if task ID doesn't exist

### Incomplete Task Command
- **Command**: `incomplete <task_id>`
- **Input**: Task ID (integer)
- **Output**: Updated task with incomplete status
- **Success Response**: "Task n marked as incomplete: ✗ [task text]"
- **Error Response**: Error if task ID doesn't exist

### Edit Task Command
- **Command**: `edit <task_id> "new task description"`
- **Input**: Task ID (integer) and new task description string
- **Output**: Updated task with new text
- **Success Response**: "Task n updated: [status] [new task text]"
- **Error Response**: Error if task ID doesn't exist or text is invalid

### List Tasks Command
- **Command**: `list`
- **Input**: None
- **Output**: Formatted list of all tasks with emoji indicators and styling
- **Success Response**: Styled list of tasks with ✓/✗ indicators
- **Error Response**: None (should always return at least an empty list)

### Delete Task Command
- **Command**: `delete <task_id>`
- **Input**: Task ID (integer)
- **Output**: Confirmation of deletion
- **Success Response**: "Task n deleted: [task text]"
- **Error Response**: Error if task ID doesn't exist

## Display Format Contract
- **Completed Tasks**: Displayed with ✓ emoji prefix
- **Incomplete Tasks**: Displayed with ✗ emoji prefix
- **Headings**: Displayed in bold text
- **Task IDs**: Clearly identified in the display
- **Colors**: Applied consistently for different elements