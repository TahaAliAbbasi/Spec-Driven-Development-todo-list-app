# Data Model: Console Todo Application

## Task Entity

### Fields
- **id**: integer (required) - Sequential identifier starting from 1
- **title**: string (required) - Task title with non-empty validation
- **description**: string (optional) - Task description, may be empty
- **is_completed**: boolean (required) - Completion status, defaults to False

### Relationships
- No external relationships - self-contained entity

### Validation Rules
- Title must not be empty or whitespace-only
- ID must be positive integer
- is_completed must be boolean value

### State Transitions
- is_completed can transition from False to True (incomplete → complete)
- is_completed can transition from True to False (complete → incomplete)

## TaskList Collection

### Structure
- In-memory list/dictionary of Task entities
- Maintains order of creation (for display purposes)
- Provides efficient lookup by ID

### Operations
- Add new Task with auto-assigned sequential ID
- Retrieve Task by ID
- Update Task fields (title, description, is_completed)
- Delete Task by ID
- List all Tasks with filtering options (all, completed, incomplete)

### Constraints
- No persistence - exists only during runtime
- No duplicate IDs allowed
- IDs increment sequentially and are never reused