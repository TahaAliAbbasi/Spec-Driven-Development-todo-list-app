# Data Model: Next.js Web Application for Todo List App

## Entity: Task

### Fields
- **id**: Integer (Primary Key, Auto-generated)
- **title**: String (Required, Max length: 255)
- **description**: String (Optional, Max length: 1000)
- **is_completed**: Boolean (Default: False)
- **created_at**: DateTime (Auto-generated timestamp)
- **updated_at**: DateTime (Auto-generated timestamp, updated on change)

### Relationships
- None (standalone entity for single-user application)

### Validation Rules
- Title must not be empty or whitespace-only
- Title must be between 1-255 characters
- Description can be empty but limited to 1000 characters if provided
- is_completed defaults to False when creating new tasks

### State Transitions
- `incomplete` → `complete`: When user marks task as complete
- `complete` → `incomplete`: When user marks task as incomplete

## Entity: TaskList (Conceptual)

### Description
Virtual collection representing all tasks for a single user (no separate entity needed as this is a single-user application)

### Access Patterns
- Retrieve all tasks
- Retrieve completed tasks
- Retrieve incomplete tasks
- Filter by title/description (future extension)

## Database Schema

### tasks table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
- Primary key index on `id`
- Index on `is_completed` for filtering
- Potential full-text index on `title` and `description` for search (future)

## API Data Structures

### Task Request (POST /tasks)
```json
{
  "title": "string (required)",
  "description": "string (optional)"
}
```

### Task Response (GET /tasks/{id})
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "is_completed": "boolean",
  "created_at": "ISO datetime string",
  "updated_at": "ISO datetime string"
}
```

### Task Update Request (PUT /tasks/{id})
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "is_completed": "boolean (optional)"
}
```

### Task List Response (GET /tasks)
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string or null",
    "is_completed": "boolean",
    "created_at": "ISO datetime string",
    "updated_at": "ISO datetime string"
  }
]
```