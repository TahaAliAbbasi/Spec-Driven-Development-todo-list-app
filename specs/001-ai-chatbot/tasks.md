# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/001-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - implementation tasks only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install OpenAI Python SDK in web_todo_app/backend: `pip install openai`
- [x] T002 [P] Install MCP SDK in web_todo_app/backend: `pip install mcp-sdk` (Note: MCP SDK not available, using standard Python)
- [x] T003 [P] Install python-dotenv in web_todo_app/backend: `pip install python-dotenv`
- [x] T004 Install OpenAI ChatKit in web_todo_app/frontend: `npm install @openai/chatkit-react`
- [x] T005 [P] Install uuid package in web_todo_app/frontend: `npm install uuid @types/uuid`
- [x] T006 Create backend chatbot directory structure: web_todo_app/backend/src/chatbot/
- [x] T007 [P] Create backend API chatbot directory structure: web_todo_app/backend/src/api/chatbot/
- [x] T008 [P] Create frontend chatbot components directory: web_todo_app/frontend/src/components/chatbot/
- [x] T009 [P] Create frontend chatbot types directory: web_todo_app/frontend/src/types/
- [x] T010 Add OpenAI API key configuration to web_todo_app/backend/.env file
- [x] T011 [P] Add chatbot session configuration to web_todo_app/backend/.env file (TTL, context window size, confidence threshold)
- [x] T012 Update web_todo_app/backend/src/config.py to load OpenAI API key and chatbot settings from environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T013 Create Intent enum and Pydantic model in web_todo_app/backend/src/chatbot/models.py
- [x] T014 [P] Create ChatMessage Pydantic model in web_todo_app/backend/src/chatbot/models.py
- [x] T015 [P] Create ChatSession Pydantic model in web_todo_app/backend/src/chatbot/models.py
- [x] T016 Create MessageSender enum in web_todo_app/backend/src/chatbot/models.py
- [x] T017 [P] Create IntentAction enum in web_todo_app/backend/src/chatbot/models.py
- [x] T018 Implement ContextManager class with MCP SDK in web_todo_app/backend/src/chatbot/context_manager.py (Note: Using standard Python instead of MCP SDK)
- [x] T019 Add session creation method to ContextManager in web_todo_app/backend/src/chatbot/context_manager.py
- [x] T020 Add session retrieval method to ContextManager in web_todo_app/backend/src/chatbot/context_manager.py
- [x] T021 Add session update method to ContextManager in web_todo_app/backend/src/chatbot/context_manager.py
- [x] T022 Add session expiry and cleanup logic to ContextManager in web_todo_app/backend/src/chatbot/context_manager.py
- [x] T023 Add context window management to ContextManager in web_todo_app/backend/src/chatbot/context_manager.py
- [x] T024 Create API request/response schemas in web_todo_app/backend/src/api/chatbot/schemas.py (MessageRequest, MessageResponse, SessionResponse, ErrorResponse)
- [x] T025 Create TypeScript type definitions in web_todo_app/frontend/src/types/chatbot.ts (MessageSender, IntentAction, ChatMessage, ChatSession, Intent enums and interfaces)
- [x] T026 Create chatbot API client service in web_todo_app/frontend/src/services/chatbot.ts with sendMessage, getSession, deleteSession methods
- [x] T027 Initialize FastAPI router for chatbot endpoints in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T028 Register chatbot router in main FastAPI app in web_todo_app/backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create new todo tasks by typing natural language commands in a chat interface

**Independent Test**: Send message "add a task to buy groceries" and verify new task appears with correct title and chatbot confirms creation

### Implementation for User Story 1

- [x] T029 [P] [US1] Create IntentParser class skeleton in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T030 [US1] Implement OpenAI Agents SDK initialization in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T031 [US1] Create system prompt for CREATE intent detection in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T032 [US1] Implement parse_intent method for CREATE action in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T033 [US1] Add entity extraction for task_title in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T034 [US1] Add confidence scoring logic in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T035 [P] [US1] Create TaskExecutor class skeleton in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T036 [US1] Implement execute_create method in TaskExecutor that calls existing TaskService in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T037 [US1] Add error handling for task creation failures in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T038 [P] [US1] Create ResponseGenerator class skeleton in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T039 [US1] Implement generate_create_response method in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T040 [US1] Add conversational response templates for CREATE success in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T041 [US1] Implement POST /api/chatbot/message endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T042 [US1] Add message validation logic in POST /api/chatbot/message endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T043 [US1] Integrate IntentParser, TaskExecutor, and ResponseGenerator in POST /api/chatbot/message endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T044 [US1] Add session management (create/update) in POST /api/chatbot/message endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T045 [P] [US1] Create ChatMessage component in web_todo_app/frontend/src/components/chatbot/ChatMessage.tsx
- [x] T046 [P] [US1] Create ChatInput component in web_todo_app/frontend/src/components/chatbot/ChatInput.tsx
- [x] T047 [P] [US1] Create ChatHistory component in web_todo_app/frontend/src/components/chatbot/ChatHistory.tsx
- [x] T048 [US1] Create ChatInterface component integrating ChatMessage, ChatInput, and ChatHistory in web_todo_app/frontend/src/components/chatbot/ChatInterface.tsx
- [x] T049 [US1] Implement useChat hook with message sending logic in web_todo_app/frontend/src/hooks/useChat.ts
- [x] T050 [US1] Add session state management to useChat hook in web_todo_app/frontend/src/hooks/useChat.ts
- [x] T051 [US1] Add message history management to useChat hook in web_todo_app/frontend/src/hooks/useChat.ts
- [x] T052 [US1] Create chat page at web_todo_app/frontend/src/pages/chat.tsx using ChatInterface component
- [x] T053 [US1] Add loading states to ChatInterface in web_todo_app/frontend/src/components/chatbot/ChatInterface.tsx
- [x] T054 [US1] Add error display to ChatInterface in web_todo_app/frontend/src/components/chatbot/ChatInterface.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via natural language

---

## Phase 4: User Story 2 - Natural Language Task Completion (Priority: P2)

**Goal**: Users can mark tasks as complete by describing them in natural language

**Independent Test**: Create task "buy milk", send message "mark buy milk as done", verify task is marked complete and chatbot confirms

### Implementation for User Story 2

- [x] T055 [US2] Add COMPLETE action to system prompt in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T056 [US2] Implement parse_intent logic for COMPLETE action in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T057 [US2] Add task matching logic by title for COMPLETE in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T058 [US2] Implement execute_complete method in TaskExecutor that calls TaskService.toggle_task_status in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T059 [US2] Add task lookup by title in execute_complete method in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T060 [US2] Add error handling for task not found in execute_complete in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T061 [US2] Implement generate_complete_response method in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T062 [US2] Add conversational response templates for COMPLETE success in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T063 [US2] Update POST /api/chatbot/message endpoint to handle COMPLETE intent in web_todo_app/backend/src/api/chatbot/routes.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Natural Language Task Querying (Priority: P3)

**Goal**: Users can ask questions about their tasks and receive conversational responses with task information

**Independent Test**: Create several tasks, send message "what tasks do I have?", verify chatbot lists all tasks with status

### Implementation for User Story 3

- [x] T064 [US3] Add READ action to system prompt in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T065 [US3] Implement parse_intent logic for READ action in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T066 [US3] Add query filter extraction (all tasks, incomplete, completed, search term) in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T067 [US3] Implement execute_read method in TaskExecutor that calls TaskService query methods in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T068 [US3] Add filtering logic (by completion status, by search term) in execute_read in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T069 [US3] Implement generate_read_response method in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T070 [US3] Add task list formatting for conversational display in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T071 [US3] Add empty result handling in generate_read_response in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T072 [US3] Update POST /api/chatbot/message endpoint to handle READ intent in web_todo_app/backend/src/api/chatbot/routes.py

**Checkpoint**: All core user stories (create, complete, query) should now be independently functional

---

## Phase 6: User Story 4 - Natural Language Task Updates (Priority: P4)

**Goal**: Users can modify existing tasks by describing changes in natural language

**Independent Test**: Create task "buy milk", send message "change buy milk to buy almond milk", verify task title is updated and chatbot confirms

### Implementation for User Story 4

- [x] T073 [US4] Add UPDATE action to system prompt in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T074 [US4] Implement parse_intent logic for UPDATE action in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T075 [US4] Add extraction for old task identifier and new task details in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T076 [US4] Implement execute_update method in TaskExecutor that calls TaskService.update_task in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T077 [US4] Add task lookup and update logic in execute_update in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T078 [US4] Add error handling for task not found in execute_update in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T079 [US4] Implement generate_update_response method in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T080 [US4] Add conversational response templates for UPDATE success in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T081 [US4] Update POST /api/chatbot/message endpoint to handle UPDATE intent in web_todo_app/backend/src/api/chatbot/routes.py

**Checkpoint**: Task creation, completion, querying, and updates all functional

---

## Phase 7: User Story 5 - Natural Language Task Deletion (Priority: P5)

**Goal**: Users can delete tasks by describing them in natural language

**Independent Test**: Create task "test task", send message "delete test task", verify task is removed and chatbot confirms deletion

### Implementation for User Story 5

- [x] T082 [US5] Add DELETE action to system prompt in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T083 [US5] Implement parse_intent logic for DELETE action in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T084 [US5] Add task identifier extraction for DELETE in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T085 [US5] Implement execute_delete method in TaskExecutor that calls TaskService.delete_task in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T086 [US5] Add task lookup and deletion logic in execute_delete in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T087 [US5] Add error handling for task not found in execute_delete in TaskExecutor in web_todo_app/backend/src/chatbot/task_executor.py
- [x] T088 [US5] Implement generate_delete_response method in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T089 [US5] Add conversational response templates for DELETE success in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T090 [US5] Update POST /api/chatbot/message endpoint to handle DELETE intent in web_todo_app/backend/src/api/chatbot/routes.py

**Checkpoint**: All user stories (P1-P5) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and complete the feature

- [x] T091 Implement GET /api/chatbot/session endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T092 [P] Implement DELETE /api/chatbot/session endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T093 [P] Add ambiguity detection logic in IntentParser (confidence < 0.7) in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T094 Implement generate_clarification_question method in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T095 Add clarification handling in POST /api/chatbot/message endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [ ] T096 [P] Add multiple task match handling in TaskExecutor (when title matches multiple tasks) in web_todo_app/backend/src/chatbot/task_executor.py
- [ ] T097 [P] Add off-topic message detection and response in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T098 Add error response templates for all error scenarios in ResponseGenerator in web_todo_app/backend/src/chatbot/response_generator.py
- [x] T099 [P] Add input sanitization in POST /api/chatbot/message endpoint in web_todo_app/backend/src/api/chatbot/routes.py
- [x] T100 [P] Add logging for all chatbot operations in web_todo_app/backend/src/chatbot/ modules
- [x] T101 Add support for 3+ phrasings per operation in system prompt in IntentParser in web_todo_app/backend/src/chatbot/intent_parser.py
- [x] T102 [P] Add navigation link to chat page in web_todo_app/frontend/src/components/ (main navigation)
- [x] T103 [P] Add responsive styling to ChatInterface for mobile devices in web_todo_app/frontend/src/components/chatbot/ChatInterface.tsx
- [ ] T104 Verify quickstart.md setup instructions work correctly
- [x] T105 [P] Add API documentation comments to all chatbot endpoints in web_todo_app/backend/src/api/chatbot/routes.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 intent parser but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Extends US1 intent parser but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Extends US1 intent parser but independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Extends US1 intent parser but independently testable

### Within Each User Story

- Backend intent parsing before task execution
- Task execution before response generation
- Backend complete before frontend integration
- Core components before page integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each user story, tasks marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch foundational models together:
Task: "Create Intent enum and Pydantic model"
Task: "Create ChatMessage Pydantic model"
Task: "Create ChatSession Pydantic model"

# Launch US1 backend modules together:
Task: "Create IntentParser class skeleton"
Task: "Create TaskExecutor class skeleton"
Task: "Create ResponseGenerator class skeleton"

# Launch US1 frontend components together:
Task: "Create ChatMessage component"
Task: "Create ChatInput component"
Task: "Create ChatHistory component"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T012)
2. Complete Phase 2: Foundational (T013-T028) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T029-T054)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Send "add a task to buy groceries"
   - Verify task created
   - Verify chatbot confirms
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add Polish → Final release
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T029-T054)
   - Developer B: User Story 2 (T055-T063)
   - Developer C: User Story 3 (T064-T072)
3. Stories complete and integrate independently
4. Continue with US4, US5, and Polish

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests included (not explicitly requested in specification)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All user stories extend the same IntentParser, TaskExecutor, and ResponseGenerator classes
- Frontend is built once in US1, reused for all other stories
- Backend endpoints handle all intents through the same POST /api/chatbot/message endpoint

---

## Summary

**Total Tasks**: 105
**Task Count by Phase**:
- Setup: 12 tasks
- Foundational: 16 tasks (BLOCKS all user stories)
- User Story 1 (P1 - MVP): 26 tasks
- User Story 2 (P2): 9 tasks
- User Story 3 (P3): 9 tasks
- User Story 4 (P4): 9 tasks
- User Story 5 (P5): 9 tasks
- Polish: 15 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1: Create task via "add a task to buy groceries"
- US2: Complete task via "mark buy milk as done"
- US3: Query tasks via "what tasks do I have?"
- US4: Update task via "change buy milk to buy almond milk"
- US5: Delete task via "delete test task"

**Suggested MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1)
