---
description: "Task list for Console Todo Application implementation"
---

# Tasks: Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo_app/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in todo_app/
- [X] T002 [P] Create models directory in todo_app/models/
- [X] T003 [P] Create services directory in todo_app/services/
- [X] T004 [P] Create cli directory in todo_app/cli/
- [X] T005 [P] Create lib directory in todo_app/lib/
- [X] T006 [P] Create tests directory structure with unit, integration, and contract subdirectories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Task model in todo_app/models/task.py
- [X] T008 Create TaskService in todo_app/services/task_service.py
- [X] T009 Create MenuHandler in todo_app/cli/menu.py
- [X] T010 Create main.py entry point with basic menu loop in todo_app/main.py
- [X] T011 Create utils module in todo_app/lib/utils.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement the ability to create new todo items with title and optional description

**Independent Test**: Can be fully tested by adding various tasks with different titles and descriptions and verifying they appear in the task list.

### Implementation for User Story 1

- [X] T012 [US1] Implement Task model with id, title, description, and is_completed attributes in todo_app/models/task.py
- [X] T013 [US1] Implement TaskService.add_task method in todo_app/services/task_service.py
- [X] T014 [US1] Implement MenuHandler.add_task_flow in todo_app/cli/menu.py
- [X] T015 [US1] Update main.py to handle menu option 1 (Add Task) and call MenuHandler
- [X] T016 [US1] Add input validation for task title in todo_app/services/task_service.py
- [X] T017 [US1] Implement sequential ID assignment in todo_app/services/task_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Implement the ability to see all tasks in a clear, readable format

**Independent Test**: Can be fully tested by adding tasks and then viewing the complete task list with proper formatting and status indicators.

### Implementation for User Story 2

- [X] T018 [US2] Implement TaskService.get_all_tasks method in todo_app/services/task_service.py
- [X] T019 [US2] Implement MenuHandler.view_tasks_flow in todo_app/cli/menu.py
- [X] T020 [US2] Update main.py to handle menu option 2 (View Task List) and call MenuHandler
- [X] T021 [US2] Implement proper task display formatting in todo_app/services/task_service.py
- [X] T022 [US2] Add visual indicators for completed vs incomplete tasks in todo_app/services/task_service.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1)

**Goal**: Implement the ability to toggle task completion status

**Independent Test**: Can be fully tested by toggling task completion status and verifying the status updates correctly in the task list.

### Implementation for User Story 5

- [X] T023 [US5] Implement TaskService.toggle_task_status method in todo_app/services/task_service.py
- [X] T024 [US5] Implement MenuHandler.mark_task_complete_flow in todo_app/cli/menu.py
- [X] T025 [US5] Update main.py to handle menu option 5 (Mark Task Complete/Incomplete) and call MenuHandler
- [X] T026 [US5] Add validation for task ID existence in todo_app/services/task_service.py

**Checkpoint**: At this point, User Stories 1, 2, and 5 should all work independently

---

## Phase 6: User Story 3 - Update Existing Tasks (Priority: P2)

**Goal**: Implement the ability to modify task details like title or description

**Independent Test**: Can be fully tested by updating task details and verifying changes persist in the task list.

### Implementation for User Story 3

- [X] T027 [US3] Implement TaskService.update_task method in todo_app/services/task_service.py
- [X] T028 [US3] Implement MenuHandler.update_task_flow in todo_app/cli/menu.py
- [X] T029 [US3] Update main.py to handle menu option 3 (Update Task) and call MenuHandler
- [X] T030 [US3] Add validation for partial updates in todo_app/services/task_service.py

**Checkpoint**: At this point, User Stories 1, 2, 5, and 3 should all work independently

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Implement the ability to remove completed or unwanted tasks

**Independent Test**: Can be fully tested by deleting tasks and verifying they no longer appear in the task list.

### Implementation for User Story 4

- [X] T031 [US4] Implement TaskService.delete_task method in todo_app/services/task_service.py
- [X] T032 [US4] Implement MenuHandler.delete_task_flow in todo_app/cli/menu.py
- [X] T033 [US4] Update main.py to handle menu option 4 (Delete Task) and call MenuHandler
- [X] T034 [US4] Add validation for task existence before deletion in todo_app/services/task_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T035 [P] Add proper error handling and validation across all service methods
- [X] T036 [P] Implement consistent error message formatting per UX contract
- [X] T037 [P] Add exit functionality with goodbye message in main.py
- [X] T038 [P] Add invalid input handling and return to main menu in all flows
- [X] T039 [P] Refactor MenuHandler to handle all menu options consistently
- [X] T040 [P] Add input validation and sanitization throughout application
- [X] T041 [P] Update all functions with proper docstrings and type hints
- [X] T042 Run final validation using quickstart.md instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch foundational components together:
Task: "Create Task model in todo_app/models/task.py"
Task: "Create TaskService in todo_app/services/task_service.py"
Task: "Create MenuHandler in todo_app/cli/menu.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 4 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 5
   - Developer D: User Story 3
   - Developer E: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence