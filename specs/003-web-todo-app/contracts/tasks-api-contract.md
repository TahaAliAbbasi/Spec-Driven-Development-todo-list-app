# API Contract: Tasks Management for Todo List App

## Base URL
```
https://api.todo-app.com/v1
```
(For development: `http://localhost:8000/v1`)

## Authentication
None required (Phase II single-user application per constitution)

## Endpoints

### GET /tasks
**Description**: Retrieve all tasks for the user

**Request**:
```
GET /tasks
Content-Type: application/json
```

**Response**:
- `200 OK` - Successful retrieval

```json
[
  {
    "id": 1,
    "title": "Complete project proposal",
    "description": "Write and submit the project proposal to stakeholders",
    "is_completed": false,
    "created_at": "2026-02-04T10:30:00Z",
    "updated_at": "2026-02-04T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Review code changes",
    "description": "Perform code review for PR #123",
    "is_completed": true,
    "created_at": "2026-02-04T09:15:00Z",
    "updated_at": "2026-02-04T09:45:00Z"
  }
]
```

### POST /tasks
**Description**: Create a new task

**Request**:
```
POST /tasks
Content-Type: application/json

{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Validation**:
- `title` is required and must not be empty or whitespace-only
- `description` is optional, max 1000 characters

**Response**:
- `201 Created` - Task successfully created
- `400 Bad Request` - Invalid input

```json
{
  "id": 3,
  "title": "New task title",
  "description": "Optional task description",
  "is_completed": false,
  "created_at": "2026-02-04T11:00:00Z",
  "updated_at": "2026-02-04T11:00:00Z"
}
```

### GET /tasks/{id}
**Description**: Retrieve a specific task by ID

**Request**:
```
GET /tasks/{id}
Content-Type: application/json
```

**Response**:
- `200 OK` - Task found
- `404 Not Found` - Task with given ID does not exist

```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the project proposal to stakeholders",
  "is_completed": false,
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T10:30:00Z"
}
```

### PUT /tasks/{id}
**Description**: Update an existing task

**Request**:
```
PUT /tasks/{id}
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated task description",
  "is_completed": true
}
```

**Validation**:
- At least one field must be provided
- If `title` is provided, it must not be empty or whitespace-only
- If `description` is provided, max 1000 characters

**Response**:
- `200 OK` - Task successfully updated
- `400 Bad Request` - Invalid input
- `404 Not Found` - Task with given ID does not exist

```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated task description",
  "is_completed": true,
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T11:15:00Z"
}
```

### PATCH /tasks/{id}/toggle-status
**Description**: Toggle the completion status of a task

**Request**:
```
PATCH /tasks/{id}/toggle-status
Content-Type: application/json
```

**Response**:
- `200 OK` - Task status successfully toggled
- `404 Not Found` - Task with given ID does not exist

```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the project proposal to stakeholders",
  "is_completed": true,
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T11:20:00Z"
}
```

### DELETE /tasks/{id}
**Description**: Delete a specific task by ID

**Request**:
```
DELETE /tasks/{id}
Content-Type: application/json
```

**Response**:
- `204 No Content` - Task successfully deleted
- `404 Not Found` - Task with given ID does not exist

## Error Responses

### General Error Format
```json
{
  "detail": "Human-readable error message"
}
```

### Common HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid request format or validation error
- `404 Not Found` - Resource does not exist
- `422 Unprocessable Entity` - Validation error with specific details
- `500 Internal Server Error` - Server error

## Request/Response Examples

### Example: Create Task
**Request**:
```
POST /tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits"
}
```

**Response (201)**:
```json
{
  "id": 4,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "is_completed": false,
  "created_at": "2026-02-04T12:00:00Z",
  "updated_at": "2026-02-04T12:00:00Z"
}
```

### Example: Update Task
**Request**:
```
PUT /tasks/4
Content-Type: application/json

{
  "is_completed": true
}
```

**Response (200)**:
```json
{
  "id": 4,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "is_completed": true,
  "created_at": "2026-02-04T12:00:00Z",
  "updated_at": "2026-02-04T12:05:00Z"
}
```