# Data Model: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot | **Date**: 2026-02-15 | **Phase**: 1 (Design)

## Overview

This document defines the data structures for the AI-powered todo chatbot feature. The data model supports natural language conversation, intent parsing, and task execution while maintaining separation from the existing task management entities.

## Entity Definitions

### 1. ChatMessage

Represents a single message in a conversation between the user and the chatbot.

**Purpose**: Store individual messages with metadata for display and context management.

**Attributes**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string (UUID) | Yes | Unique message identifier | UUID v4 format |
| session_id | string (UUID) | Yes | Reference to parent session | UUID v4 format |
| sender | enum | Yes | Message sender | "user" or "bot" |
| content | string | Yes | Message text content | 1-2000 characters |
| timestamp | datetime | Yes | Message creation time | ISO 8601 format |
| intent | Intent (optional) | No | Parsed intent (bot messages only) | See Intent entity |
| metadata | object (optional) | No | Additional message data | JSON object |

**Relationships**:
- Belongs to one ChatSession (many-to-one)
- May reference one Intent (one-to-one, optional)

**State Transitions**: None (immutable after creation)

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "sender": "user",
  "content": "add a task to buy groceries",
  "timestamp": "2026-02-15T14:30:00Z",
  "intent": null,
  "metadata": {}
}
```

**Storage**: In-memory (session-scoped, not persisted to database)

---

### 2. ChatSession

Represents a conversation session containing message history and context.

**Purpose**: Manage conversation state, context window, and session lifecycle.

**Attributes**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string (UUID) | Yes | Unique session identifier | UUID v4 format |
| messages | array[ChatMessage] | Yes | Ordered message history | Max 50 messages |
| context_window | array[ChatMessage] | Yes | Recent messages for AI context | Max 10 messages |
| created_at | datetime | Yes | Session creation time | ISO 8601 format |
| last_activity | datetime | Yes | Last message timestamp | ISO 8601 format |
| expires_at | datetime | Yes | Session expiry time | created_at + TTL |
| metadata | object (optional) | No | Session-level data | JSON object |

**Relationships**:
- Has many ChatMessages (one-to-many)

**State Transitions**:
- `active` → Session is valid and accepting messages
- `expired` → Session has exceeded TTL, should be cleaned up

**Lifecycle**:
1. Created on first user message
2. Updated on each message exchange
3. Expires after 30 minutes of inactivity (configurable)
4. Cleaned up by background task

**Example**:
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "messages": [
    {"id": "...", "sender": "user", "content": "add task..."},
    {"id": "...", "sender": "bot", "content": "I've added..."}
  ],
  "context_window": [
    {"id": "...", "sender": "user", "content": "add task..."}
  ],
  "created_at": "2026-02-15T14:00:00Z",
  "last_activity": "2026-02-15T14:30:00Z",
  "expires_at": "2026-02-15T15:00:00Z",
  "metadata": {}
}
```

**Storage**: In-memory Python dict, keyed by session_id

---

### 3. Intent

Represents a parsed user intent with extracted parameters.

**Purpose**: Structure the output of intent parsing for task execution.

**Attributes**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| action | enum | Yes | Intent action type | CREATE, READ, UPDATE, DELETE, COMPLETE |
| confidence | float | Yes | Parsing confidence score | 0.0 to 1.0 |
| task_id | integer (optional) | No | Target task ID (for UPDATE, DELETE, COMPLETE) | Positive integer |
| task_title | string (optional) | No | Task title (for CREATE, UPDATE) | 1-200 characters |
| task_description | string (optional) | No | Task description (for CREATE, UPDATE) | 0-1000 characters |
| query_filter | object (optional) | No | Query parameters (for READ) | JSON object |
| ambiguous | boolean | Yes | Whether intent is ambiguous | true/false |
| clarification_needed | string (optional) | No | Clarification question if ambiguous | 1-500 characters |

**Relationships**:
- May be referenced by one ChatMessage (one-to-one)

**Validation Rules**:
- If `action` is CREATE: `task_title` is required
- If `action` is UPDATE, DELETE, or COMPLETE: `task_id` or `task_title` is required
- If `ambiguous` is true: `clarification_needed` must be provided
- If `confidence` < 0.7: `ambiguous` should be true

**Example (CREATE)**:
```json
{
  "action": "CREATE",
  "confidence": 0.95,
  "task_id": null,
  "task_title": "buy groceries",
  "task_description": null,
  "query_filter": null,
  "ambiguous": false,
  "clarification_needed": null
}
```

**Example (COMPLETE)**:
```json
{
  "action": "COMPLETE",
  "confidence": 0.88,
  "task_id": null,
  "task_title": "buy groceries",
  "task_description": null,
  "query_filter": null,
  "ambiguous": false,
  "clarification_needed": null
}
```

**Example (Ambiguous)**:
```json
{
  "action": "UPDATE",
  "confidence": 0.45,
  "task_id": null,
  "task_title": null,
  "task_description": null,
  "query_filter": null,
  "ambiguous": true,
  "clarification_needed": "Which task would you like to update?"
}
```

**Storage**: Transient (created during request processing, not persisted)

---

### 4. Task (Existing Entity - No Changes)

**Reference**: Existing Phase II entity, defined in `web_todo_app/backend/src/models/task.py`

**Attributes** (for reference):
- `id`: integer (primary key)
- `title`: string
- `description`: string (optional)
- `is_completed`: boolean
- `created_at`: datetime
- `updated_at`: datetime

**Note**: The chatbot feature does NOT modify the Task entity schema. All task operations use the existing TaskService interface.

---

## Entity Relationships

```
ChatSession (1) ──< (many) ChatMessage
ChatMessage (1) ──< (0..1) Intent
Intent (0..many) ──> (0..1) Task [reference only, no FK]
```

**Explanation**:
- One ChatSession contains many ChatMessages
- Each ChatMessage may have one Intent (bot messages with parsed intent)
- Intents may reference Tasks by ID or title, but no foreign key relationship (loose coupling)

---

## Data Flow

### Message Processing Flow

```
1. User Input
   ↓
2. Create ChatMessage (sender: "user")
   ↓
3. Add to ChatSession.messages
   ↓
4. Update ChatSession.context_window
   ↓
5. Parse Intent from message + context
   ↓
6. Execute Task Operation (if intent clear)
   ↓
7. Generate Response
   ↓
8. Create ChatMessage (sender: "bot", intent: Intent)
   ↓
9. Add to ChatSession.messages
   ↓
10. Return Response to Frontend
```

### Context Window Management

```
ChatSession.messages: [M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12]
                                                              ↑
ChatSession.context_window: [M3, M4, M5, M6, M7, M8, M9, M10, M11, M12]
                            └─────────── Last 10 messages ──────────────┘
```

**Rules**:
- `messages` array stores all messages (up to 50, then FIFO eviction)
- `context_window` stores last 10 messages for AI context
- When `messages` exceeds 50, remove oldest messages
- `context_window` always reflects the most recent 10 messages

---

## Validation Rules

### ChatMessage Validation
- `content` must not be empty or whitespace-only
- `content` length: 1-2000 characters
- `sender` must be exactly "user" or "bot"
- `timestamp` must be valid ISO 8601 datetime

### ChatSession Validation
- `messages` array must be ordered by timestamp (ascending)
- `context_window` must be a subset of `messages`
- `expires_at` must be after `created_at`
- `last_activity` must be >= `created_at`

### Intent Validation
- `action` must be one of: CREATE, READ, UPDATE, DELETE, COMPLETE
- `confidence` must be between 0.0 and 1.0
- If `action` is CREATE: `task_title` is required
- If `action` is UPDATE/DELETE/COMPLETE: `task_id` or `task_title` is required
- If `ambiguous` is true: `clarification_needed` must be provided

---

## Storage Strategy

### In-Memory Storage (Phase III)

**Implementation**: Python dictionary
```python
sessions: Dict[str, ChatSession] = {}
```

**Key**: session_id (UUID string)
**Value**: ChatSession object

**Lifecycle**:
- Created on first message
- Updated on each message exchange
- Expired after TTL (30 minutes default)
- Cleaned up by background task (runs every 5 minutes)

**Limitations**:
- Lost on server restart (acceptable for Phase III)
- Not shared across multiple server instances (single instance only)
- No persistence across browser sessions

**Future Considerations** (Phase IV/V):
- Redis for distributed sessions
- Database persistence for conversation history
- Multi-instance support with shared state

---

## Type Definitions

### TypeScript (Frontend)

```typescript
// types/chatbot.ts

export enum MessageSender {
  User = "user",
  Bot = "bot"
}

export enum IntentAction {
  CREATE = "CREATE",
  READ = "READ",
  UPDATE = "UPDATE",
  DELETE = "DELETE",
  COMPLETE = "COMPLETE"
}

export interface ChatMessage {
  id: string;
  session_id: string;
  sender: MessageSender;
  content: string;
  timestamp: string; // ISO 8601
  intent?: Intent;
  metadata?: Record<string, any>;
}

export interface ChatSession {
  id: string;
  messages: ChatMessage[];
  context_window: ChatMessage[];
  created_at: string; // ISO 8601
  last_activity: string; // ISO 8601
  expires_at: string; // ISO 8601
  metadata?: Record<string, any>;
}

export interface Intent {
  action: IntentAction;
  confidence: number;
  task_id?: number;
  task_title?: string;
  task_description?: string;
  query_filter?: Record<string, any>;
  ambiguous: boolean;
  clarification_needed?: string;
}
```

### Python (Backend)

```python
# backend/src/chatbot/models.py

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator

class MessageSender(str, Enum):
    USER = "user"
    BOT = "bot"

class IntentAction(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    COMPLETE = "COMPLETE"

class Intent(BaseModel):
    action: IntentAction
    confidence: float = Field(ge=0.0, le=1.0)
    task_id: Optional[int] = None
    task_title: Optional[str] = Field(None, min_length=1, max_length=200)
    task_description: Optional[str] = Field(None, max_length=1000)
    query_filter: Optional[Dict[str, Any]] = None
    ambiguous: bool
    clarification_needed: Optional[str] = Field(None, max_length=500)

class ChatMessage(BaseModel):
    id: str
    session_id: str
    sender: MessageSender
    content: str = Field(min_length=1, max_length=2000)
    timestamp: datetime
    intent: Optional[Intent] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatSession(BaseModel):
    id: str
    messages: List[ChatMessage] = Field(default_factory=list, max_items=50)
    context_window: List[ChatMessage] = Field(default_factory=list, max_items=10)
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    metadata: Optional[Dict[str, Any]] = None
```

---

## Summary

**Entities Defined**: 3 new entities (ChatMessage, ChatSession, Intent) + 1 existing reference (Task)

**Storage**: In-memory (session-scoped, no database persistence)

**Relationships**: ChatSession → ChatMessage → Intent → Task (reference)

**Validation**: Comprehensive validation rules for all entities

**Type Safety**: Full TypeScript and Python type definitions provided

**Ready for**: API contract definition (contracts/)

---

**Data Model Status**: ✅ Complete
**Next Step**: Generate API contracts (Phase 1)
