# Quickstart Guide: Next.js Web Application for Todo List App

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- npm or yarn
- PostgreSQL-compatible database (Neon DB recommended)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Update DATABASE_URL in .env with your Neon DB connection string

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
# Open new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.local.example .env.local
# Update NEXT_PUBLIC_API_BASE_URL if backend is running on different port

# Start the development server
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

## Development Commands

### Backend
```bash
# Run tests
pytest

# Run with auto-reload
uvicorn src.main:app --reload

# Format code
black src/
isort src/

# Check types
mypy src/
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run linting
npm run lint

# Run type checking
npm run type-check
```

## Folder Structure Overview

### Backend
```
backend/
├── src/
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   ├── api/             # API routes
│   └── main.py          # Application entry point
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── alembic/             # Database migrations
```

### Frontend
```
frontend/
├── src/
│   ├── components/      # Reusable React components
│   ├── pages/           # Next.js pages
│   ├── services/        # API clients and utilities
│   └── styles/          # CSS and styling
├── public/              # Static assets
├── package.json         # Node.js dependencies
└── next.config.js       # Next.js configuration
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Database Setup

1. Sign up for Neon DB (https://neon.tech)
2. Create a new project
3. Copy the connection string and update DATABASE_URL in backend/.env
4. Run migrations: `alembic upgrade head`

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_task_service.py
```

### Frontend Tests
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run end-to-end tests
npm run test:e2e
```

## API Endpoints

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

Key endpoints:
- GET `/v1/tasks` - List all tasks
- POST `/v1/tasks` - Create a new task
- GET `/v1/tasks/{id}` - Get specific task
- PUT `/v1/tasks/{id}` - Update task
- PATCH `/v1/tasks/{id}/toggle-status` - Toggle completion status
- DELETE `/v1/tasks/{id}` - Delete task

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check if Python environment is activated
- Verify dependencies are installed: `pip install -r requirements.txt`
- Ensure database connection is working

**Frontend can't connect to backend:**
- Verify backend is running on http://localhost:8000
- Check NEXT_PUBLIC_API_BASE_URL in frontend/.env.local
- Ensure CORS is configured correctly

**Database connection errors:**
- Verify DATABASE_URL in backend/.env
- Ensure database service is running
- Run migrations: `alembic upgrade head`

## Next Steps

1. Implement the basic task operations (CRUD)
2. Add responsive design for mobile support
3. Implement proper error handling
4. Add loading states and optimistic updates
5. Set up automated testing pipeline