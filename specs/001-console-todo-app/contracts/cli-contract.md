# CLI Contract: Console Todo Application

## Menu Interface Contract

### Main Menu Options
The application MUST display exactly the following menu:
```
TODO APPLICATION
================
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit
Choose an option (1-6):
```

### Input/Output Specifications

#### Add Task Flow
**Input**:
- Menu selection: "1"
- Title prompt: "Enter task title: "
- Optional description prompt: "Enter task description (press Enter to skip): "

**Output**:
- Success: Task added with sequential ID
- Error: "Error: Task title cannot be empty."

#### View Task List Flow
**Input**:
- Menu selection: "2"

**Output**:
- Task display format: "{ID}. [{X if completed}] {Title} - {Description}"
- Where [X] appears only if task is completed
- Empty list shows appropriate message

#### Update Task Flow
**Input**:
- Menu selection: "3"
- ID prompt: "Enter task ID to update: "
- Title prompt: "Enter new title (press Enter to keep current): "
- Description prompt: "Enter new description (press Enter to keep current): "

**Output**:
- Success: Task updated
- Error: "Error: Task with ID [ID] does not exist."

#### Delete Task Flow
**Input**:
- Menu selection: "4"
- ID prompt: "Enter task ID to delete: "

**Output**:
- Success: Task removed
- Error: "Error: Task with ID [ID] does not exist."

#### Mark Complete Flow
**Input**:
- Menu selection: "5"
- ID prompt: "Enter task ID to toggle completion status: "

**Output**:
- Success: Task status toggled
- Error: "Error: Task with ID [ID] does not exist."

#### Exit Flow
**Input**:
- Menu selection: "6"

**Output**:
- Message: "Thank you for using the Todo Application. Goodbye!"
- Program termination

### Error Handling Contract
All errors MUST follow the pattern: "Error: [specific message]"
The application MUST return to main menu after displaying error message (except for Exit)

### State Persistence Contract
- All data exists only in memory during runtime
- No data persists after program termination
- Sequential IDs continue incrementing across the session