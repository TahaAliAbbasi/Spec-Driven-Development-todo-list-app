# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot | **Date**: 2026-02-15 | **Phase**: 1 (Design)

## Overview

This guide helps developers set up and run the AI-powered todo chatbot feature locally. The chatbot extends the existing Phase II web application with natural language task management capabilities.

## Prerequisites

### Required Software
- **Node.js**: 18.x or higher
- **Python**: 3.11 or higher
- **npm**: 9.x or higher
- **pip**: Latest version

### Existing Setup
- Phase II web application must be functional
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`
- Neon DB connection configured and working

### API Keys
- **OpenAI API Key OR OpenRouter API Key**: Required for intent parsing and response generation
  - **Option 1 - OpenAI**: Sign up at https://platform.openai.com/
  - **Option 2 - OpenRouter**: Sign up at https://openrouter.ai/ (supports multiple models including free options)
  - Create an API key in the dashboard
  - Ensure you have credits available (or use free models with OpenRouter)

## Installation

### 1. Backend Setup

#### Install Python Dependencies

```bash
cd web_todo_app/backend

# Install OpenAI SDK
pip install openai

# Install MCP SDK
pip install mcp-sdk

# Install additional dependencies
pip install python-dotenv  # For environment variable management
```

#### Configure Environment Variables

Create or update `.env` file in `web_todo_app/backend/`:

```bash
# Existing variables (from Phase II)
DATABASE_URL=postgresql://...

# New variables for Phase III
OPENAI_API_KEY=sk-...  # Your OpenAI API key
CHATBOT_SESSION_TTL=1800  # Session expiry in seconds (30 minutes)
CHATBOT_MAX_CONTEXT_MESSAGES=10  # Context window size
CHATBOT_INTENT_CONFIDENCE_THRESHOLD=0.7  # Minimum confidence for clear intent
```

**Security Note**: Never commit `.env` file to version control. Ensure `.env` is in `.gitignore`.

#### Verify Backend Installation

```bash
# Run backend tests (after implementation)
pytest tests/unit/chatbot/ -v
pytest tests/integration/chatbot/ -v

# Start backend server
uvicorn src.main:app --reload --port 8000
```

### 2. Frontend Setup

#### Install Node Dependencies

```bash
cd web_todo_app/frontend

# Install OpenAI ChatKit
npm install @openai/chatkit-react

# Install additional dependencies
npm install uuid  # For generating session IDs
npm install @types/uuid --save-dev  # TypeScript types
```

#### Verify Frontend Installation

```bash
# Run frontend tests (after implementation)
npm test -- chatbot

# Start frontend development server
npm run dev
```

### 3. Verify Integration

#### Check Backend Health

```bash
# Test backend is running
curl http://localhost:8000/health

# Test chatbot endpoint (after implementation)
curl -X POST http://localhost:8000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "add a task to test the chatbot"}'
```

#### Check Frontend Access

1. Open browser to `http://localhost:3000`
2. Navigate to `/chat` (new chatbot page)
3. Verify chat interface loads without errors

## Development Workflow

### Running the Application

#### Terminal 1: Backend
```bash
cd web_todo_app/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000
```

#### Terminal 2: Frontend
```bash
cd web_todo_app/frontend
npm run dev
```

#### Terminal 3: Tests (optional)
```bash
# Backend tests
cd web_todo_app/backend
pytest --watch

# Frontend tests
cd web_todo_app/frontend
npm test -- --watch
```

### Testing the Chatbot

#### Manual Testing Scenarios

**Scenario 1: Create Task**
1. Open chat interface at `http://localhost:3000/chat`
2. Type: "add a task to buy groceries"
3. Expected: Bot responds "I've added 'buy groceries' to your task list."
4. Verify: Check task list page, new task should appear

**Scenario 2: Complete Task**
1. Type: "mark buy groceries as done"
2. Expected: Bot responds "I've marked 'buy groceries' as complete."
3. Verify: Task should be marked complete in task list

**Scenario 3: Query Tasks**
1. Type: "what tasks do I have?"
2. Expected: Bot lists all tasks with their status
3. Verify: Response includes all existing tasks

**Scenario 4: Ambiguous Intent**
1. Create multiple tasks with "report" in title
2. Type: "complete the report"
3. Expected: Bot asks "Which task would you like to complete?" with options
4. Verify: Clarification question is displayed

**Scenario 5: Error Handling**
1. Type: "complete nonexistent task"
2. Expected: Bot responds "I couldn't find a task matching that description."
3. Verify: User-friendly error message, no crash

#### Automated Testing

```bash
# Run all chatbot tests
cd web_todo_app/backend
pytest tests/chatbot/ -v --cov=src/chatbot

cd web_todo_app/frontend
npm test -- chatbot --coverage
```

## Project Structure

### Backend Files (New)

```
web_todo_app/backend/
├── src/
│   ├── api/
│   │   └── chatbot/
│   │       ├── __init__.py
│   │       ├── routes.py          # FastAPI endpoints
│   │       └── schemas.py         # Pydantic models
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── intent_parser.py       # OpenAI Agents SDK integration
│   │   ├── task_executor.py       # Task operation execution
│   │   ├── response_generator.py  # Conversational response generation
│   │   └── context_manager.py     # MCP SDK session management
│   └── config.py                  # Add OPENAI_API_KEY config
└── tests/
    ├── unit/chatbot/
    │   ├── test_intent_parser.py
    │   ├── test_task_executor.py
    │   └── test_response_generator.py
    └── integration/chatbot/
        └── test_chatbot_flow.py
```

### Frontend Files (New)

```
web_todo_app/frontend/
├── src/
│   ├── components/chatbot/
│   │   ├── ChatInterface.tsx      # Main chat container
│   │   ├── ChatMessage.tsx        # Individual message component
│   │   ├── ChatInput.tsx          # Message input field
│   │   └── ChatHistory.tsx        # Message list display
│   ├── pages/
│   │   └── chat.tsx               # Chat page route
│   ├── services/
│   │   └── chatbot.ts             # API client for chatbot endpoints
│   ├── hooks/
│   │   └── useChat.ts             # Chat state management hook
│   └── types/
│       └── chatbot.ts             # TypeScript type definitions
└── tests/chatbot/
    ├── ChatInterface.test.tsx
    └── useChat.test.ts
```

## Common Issues & Troubleshooting

### Issue: "OpenAI API key not found"

**Symptom**: Backend returns 500 error when sending messages

**Solution**:
1. Verify `.env` file exists in `web_todo_app/backend/`
2. Check `OPENAI_API_KEY` is set correctly
3. Restart backend server after updating `.env`

```bash
# Verify environment variable is loaded
cd web_todo_app/backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Issue: "Session expired" errors

**Symptom**: Chat session resets unexpectedly

**Solution**:
- Sessions expire after 30 minutes of inactivity (by design)
- Adjust `CHATBOT_SESSION_TTL` in `.env` if needed
- Note: Session storage is in-memory, lost on server restart

### Issue: Intent parsing accuracy is low

**Symptom**: Bot frequently asks for clarification or misunderstands commands

**Solution**:
1. Check OpenAI API status: https://status.openai.com/
2. Review system prompt in `intent_parser.py`
3. Add more examples to few-shot learning
4. Adjust `CHATBOT_INTENT_CONFIDENCE_THRESHOLD` (lower = more lenient)

### Issue: Frontend can't connect to backend

**Symptom**: Network errors in browser console

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration in backend
3. Verify frontend API base URL in `chatbot.ts`

### Issue: Chat interface not rendering

**Symptom**: Blank page or component errors

**Solution**:
1. Check browser console for errors
2. Verify ChatKit installation: `npm list @openai/chatkit-react`
3. Clear node_modules and reinstall: `rm -rf node_modules && npm install`

## API Testing with curl

### Send a message

```bash
curl -X POST http://localhost:8000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "message": "add a task to buy groceries"
  }'
```

### Get session info

```bash
curl "http://localhost:8000/api/chatbot/session?session_id=7c9e6679-7425-40de-944b-e07fc1f90ae7"
```

### Delete session

```bash
curl -X DELETE "http://localhost:8000/api/chatbot/session?session_id=7c9e6679-7425-40de-944b-e07fc1f90ae7"
```

## Performance Monitoring

### Backend Metrics

Monitor these metrics during development:

- **Intent parsing time**: Should be <500ms
- **Total response time**: Should be <2 seconds (95th percentile)
- **OpenAI API calls**: Track rate limits and costs
- **Session count**: Monitor memory usage

### Frontend Metrics

- **Chat interface render time**: Should be <100ms
- **Message send latency**: Should feel instant (<200ms perceived)
- **UI responsiveness**: No blocking during API calls

## Next Steps

After completing the quickstart setup:

1. **Run `/sp.tasks`**: Generate implementation tasks
2. **Review tasks.md**: Understand implementation order
3. **Run `/sp.implement`**: Begin implementation
4. **Test continuously**: Run tests after each task completion
5. **Iterate**: Refine based on test results and user feedback

## Additional Resources

- **OpenAI API Documentation**: https://platform.openai.com/docs
- **ChatKit Documentation**: https://github.com/openai/chatkit-react
- **MCP SDK Documentation**: https://modelcontextprotocol.io/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs

## Support

For issues specific to this feature:
1. Check this quickstart guide
2. Review [research.md](./research.md) for technical decisions
3. Review [data-model.md](./data-model.md) for entity definitions
4. Review [contracts/](./contracts/) for API specifications

---

**Quickstart Status**: ✅ Complete
**Next Step**: Update agent context (Phase 1)
