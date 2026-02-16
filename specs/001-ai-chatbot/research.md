# Research: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot | **Date**: 2026-02-15 | **Phase**: 0 (Research)

## Purpose

This document consolidates research findings for implementing the AI-powered todo chatbot. All technical decisions and best practices are documented here to resolve uncertainties identified in the implementation plan.

## Research Areas

### 1. OpenAI ChatKit Integration

**Research Question**: How to integrate ChatKit into Next.js frontend?

**Findings**:
- OpenAI ChatKit is a React-based UI library for building chat interfaces
- Installation: `npm install @openai/chatkit-react`
- Provides pre-built components: `<ChatContainer>`, `<MessageList>`, `<MessageInput>`
- Supports custom styling and theming
- Handles message rendering, input validation, and scroll management

**Decision**: Use ChatKit's pre-built components with custom styling to match existing app design

**Rationale**: Reduces development time, provides battle-tested UI patterns, aligns with Phase III constitutional requirement

**Alternatives Considered**:
- Custom React components: More control but higher development effort
- Third-party chat libraries: Not aligned with constitutional requirement for OpenAI ChatKit

---

**Research Question**: ChatKit conversation state management patterns?

**Findings**:
- ChatKit uses React Context API for state management
- Provides `useChatContext()` hook for accessing conversation state
- State includes: messages array, loading status, error state
- Supports optimistic updates for better UX
- Can integrate with external state management (Redux, Zustand)

**Decision**: Use ChatKit's built-in state management with React hooks

**Rationale**: Simplest approach, no additional dependencies, sufficient for Phase III scope

**Alternatives Considered**:
- Redux integration: Overkill for single-page chat feature
- Zustand: Adds complexity without clear benefit for this use case

---

**Research Question**: ChatKit API authentication and configuration?

**Findings**:
- ChatKit requires OpenAI API key for backend communication
- Frontend should NOT contain API keys (security risk)
- Backend proxy pattern: Frontend → Backend → OpenAI API
- Configuration via environment variables: `OPENAI_API_KEY`
- Supports custom API endpoints for proxying

**Decision**: Implement backend proxy for OpenAI API calls, store API key in backend environment variables

**Rationale**: Security best practice, prevents API key exposure, allows rate limiting and monitoring

**Alternatives Considered**:
- Client-side API key: Security vulnerability, rejected
- Serverless functions: Adds infrastructure complexity (Phase IV/V only)

### 2. OpenAI Agents SDK Usage

**Research Question**: Best practices for intent parsing with Agents SDK?

**Findings**:
- Agents SDK provides structured output via function calling
- Define intent schema as TypeScript/Python types
- Use system prompts to guide intent classification
- Supports multi-step reasoning for complex intents
- Provides built-in error handling and retries

**Decision**: Define intent schema with action types (CREATE, READ, UPDATE, DELETE, COMPLETE) and use function calling for structured extraction

**Rationale**: Type-safe intent parsing, reduces ambiguity, enables validation

**Alternatives Considered**:
- Regex-based parsing: Brittle, doesn't handle variations well
- Simple text classification: Less structured, harder to validate

---

**Research Question**: How to structure agent prompts for task management domain?

**Findings**:
- System prompt should define agent role and capabilities
- Include examples of valid intents and expected outputs
- Use few-shot learning for better accuracy
- Specify output format explicitly (JSON schema)
- Include error handling instructions

**Decision**: Create domain-specific system prompt with task management examples and JSON schema for intent output

**Rationale**: Improves intent accuracy (90% requirement), provides consistent output format

**Example System Prompt Structure**:
```
You are a task management assistant. Parse user messages to identify their intent.

Valid actions: CREATE, READ, UPDATE, DELETE, COMPLETE
Output format: {"action": "CREATE", "task_title": "...", "task_description": "..."}

Examples:
- "add a task to buy groceries" → {"action": "CREATE", "task_title": "buy groceries"}
- "mark buy milk as done" → {"action": "COMPLETE", "task_title": "buy milk"}
```

---

**Research Question**: Error handling patterns in Agents SDK?

**Findings**:
- SDK throws typed exceptions for different error scenarios
- Common errors: API rate limits, invalid responses, timeout
- Supports retry logic with exponential backoff
- Provides error context for debugging
- Can implement custom error handlers

**Decision**: Implement try-catch blocks with specific error types, provide user-friendly error messages, log errors for debugging

**Rationale**: Meets reliability requirements, improves user experience, enables troubleshooting

### 3. MCP SDK Implementation

**Research Question**: MCP SDK setup for conversation context management?

**Findings**:
- MCP (Model Context Protocol) SDK manages conversation history
- Installation: `pip install mcp-sdk` (Python), `npm install @modelcontextprotocol/sdk` (TypeScript)
- Provides context window management (token limits)
- Supports context compression for long conversations
- Handles message history persistence

**Decision**: Use MCP SDK for managing conversation context with in-memory storage (session-scoped)

**Rationale**: Constitutional requirement, proper context protocol, handles token limits automatically

**Alternatives Considered**:
- Manual context management: Error-prone, doesn't handle token limits
- Database persistence: Out of scope for Phase III (session storage only)

---

**Research Question**: Session state persistence patterns (in-memory for Phase III)?

**Findings**:
- In-memory storage: Python dict or JavaScript Map
- Session identified by unique session ID (UUID)
- Automatic cleanup for expired sessions (TTL pattern)
- No persistence across server restarts (acceptable for Phase III)

**Decision**: Use Python dict with session ID keys, implement TTL-based cleanup (30 minute expiry)

**Rationale**: Simple, meets Phase III requirements, no infrastructure complexity

**Alternatives Considered**:
- Redis: Adds infrastructure complexity (Phase IV/V)
- Database: Out of scope for Phase III

---

**Research Question**: Context window management for multi-turn conversations?

**Findings**:
- OpenAI models have token limits (e.g., 4096, 8192, 16384)
- MCP SDK provides automatic context pruning
- Strategies: sliding window, summarization, priority-based retention
- Should retain recent messages and critical context

**Decision**: Use MCP SDK's automatic context pruning with sliding window (keep last 10 messages)

**Rationale**: Prevents token limit errors, maintains conversation continuity, simple implementation

### 4. Intent Classification Patterns

**Research Question**: Common NLP patterns for CRUD operation detection?

**Findings**:
- Action verbs indicate intent: "add", "create", "new" → CREATE
- Completion verbs: "done", "complete", "finish" → COMPLETE
- Query verbs: "show", "list", "what" → READ
- Modification verbs: "change", "update", "edit" → UPDATE
- Deletion verbs: "delete", "remove", "clear" → DELETE

**Decision**: Use Agents SDK function calling with action verb examples in system prompt

**Rationale**: Handles variations naturally, extensible for new phrasings

---

**Research Question**: Entity extraction techniques for task titles/descriptions?

**Findings**:
- Named entity recognition (NER) for extracting task details
- Pattern: "add a task to [TASK_TITLE]"
- Pattern: "create task: [TASK_TITLE]"
- Pattern: "remind me to [TASK_TITLE]"
- Agents SDK can extract entities via function parameters

**Decision**: Define function parameters for task_title and task_description, let Agents SDK extract entities

**Rationale**: Leverages SDK capabilities, handles variations, type-safe extraction

---

**Research Question**: Ambiguity resolution strategies?

**Findings**:
- When intent unclear: ask clarifying question
- When multiple tasks match: show options, ask user to select
- When missing required info: prompt for missing details
- Use confidence scores to detect ambiguity

**Decision**: Implement clarification flow - if intent confidence <0.7 or required fields missing, ask follow-up question

**Rationale**: Meets FR-006 requirement (handle ambiguous input), improves accuracy

### 5. Backend Integration Architecture

**Research Question**: How to call existing FastAPI endpoints from chatbot service?

**Findings**:
- Internal function calls: Import TaskService directly (same process)
- No HTTP overhead for internal calls
- Reuse existing business logic and validation
- Share database session for transactional consistency

**Decision**: Import and use TaskService directly in chatbot task_executor module

**Rationale**: Simplest approach, no HTTP overhead, maintains separation of concerns

**Alternatives Considered**:
- HTTP calls to own API: Unnecessary overhead, same process
- Duplicate task logic: Violates DRY principle, maintenance burden

---

**Research Question**: Error propagation from task service to chatbot responses?

**Findings**:
- TaskService raises exceptions for errors (e.g., TaskNotFound, ValidationError)
- Chatbot should catch exceptions and convert to user-friendly messages
- Preserve error context for logging
- Different error types need different user messages

**Decision**: Implement error mapping in response_generator - map exception types to conversational error messages

**Rationale**: User-friendly error handling, maintains technical error context for debugging

**Example Mapping**:
- `TaskNotFound` → "I couldn't find a task matching that description. Could you be more specific?"
- `ValidationError` → "That task information doesn't look quite right. Could you try again?"

---

**Research Question**: API client patterns in Python?

**Findings**:
- For OpenAI API: Use official `openai` Python library
- Async/await for non-blocking API calls
- Connection pooling for efficiency
- Timeout configuration to prevent hanging

**Decision**: Use `openai` Python library with async/await, configure 5-second timeout

**Rationale**: Official library, well-maintained, supports async operations

## Technology Stack Summary

### Frontend
- **Framework**: Next.js 14+ with React 18+
- **Chat UI**: OpenAI ChatKit (`@openai/chatkit-react`)
- **State Management**: React hooks + ChatKit context
- **HTTP Client**: Fetch API (built-in)
- **Testing**: Jest + React Testing Library

### Backend
- **Framework**: FastAPI (existing)
- **AI Integration**: OpenAI Python SDK (`openai`)
- **Context Management**: MCP SDK (`mcp-sdk`)
- **Session Storage**: In-memory Python dict with TTL
- **Testing**: pytest (existing)

### Configuration
- **Environment Variables**:
  - `OPENAI_API_KEY`: OpenAI API authentication
  - `CHATBOT_SESSION_TTL`: Session expiry time (default: 1800 seconds)
  - `CHATBOT_MAX_CONTEXT_MESSAGES`: Context window size (default: 10)

## Implementation Patterns

### Intent Parsing Flow
1. User sends message → Frontend
2. Frontend → Backend `/api/chatbot/message`
3. Backend retrieves session context (MCP SDK)
4. Backend calls Agents SDK with message + context
5. Agents SDK returns structured intent
6. Backend validates intent and extracts parameters
7. If ambiguous → return clarification question
8. If clear → proceed to execution

### Task Execution Flow
1. Intent parser returns validated intent
2. Task executor maps intent to TaskService method
3. Call TaskService method (internal function call)
4. Handle success/error responses
5. Response generator creates conversational message
6. Update session context with message history
7. Return response to frontend

### Error Handling Pattern
```python
try:
    intent = await parse_intent(message, context)
    result = await execute_task(intent)
    response = generate_response(result)
except AmbiguousIntentError as e:
    response = generate_clarification_question(e)
except TaskNotFoundError as e:
    response = generate_friendly_error("task_not_found")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    response = generate_friendly_error("generic")
```

## Open Questions Resolved

All research questions from the implementation plan have been addressed. No remaining uncertainties for Phase 1 design.

## Next Steps

1. ✅ Research complete
2. ⏳ Generate data-model.md (Phase 1)
3. ⏳ Generate API contracts (Phase 1)
4. ⏳ Generate quickstart.md (Phase 1)
5. ⏳ Update agent context (Phase 1)

---

**Research Status**: ✅ Complete
**Decisions Made**: 15 technical decisions documented
**Ready for Phase 1**: Yes
