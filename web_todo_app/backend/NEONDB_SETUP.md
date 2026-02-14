# NeonDB Integration Setup Guide

## Overview

This guide explains how to set up and use NeonDB (PostgreSQL) with the Todo List web application. The application has been updated to support both SQLite (for development) and NeonDB (for production).

## Prerequisites

- Python 3.11 or higher
- Access to a NeonDB PostgreSQL database
- NeonDB connection string with SSL parameters

## Environment Configuration

### Setting the Database URL

The application uses the `DATABASE_URL` environment variable to determine which database to connect to.

**For NeonDB (Production):**
```bash
export DATABASE_URL="postgresql://neondb_owner:npg_WnSvVz2DYH7k@ep-withered-shape-ainx0eeh-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

**For SQLite (Development):**
```bash
# Leave DATABASE_URL unset, or explicitly set it:
export DATABASE_URL="sqlite:///./todo_app.db"
```

### Connection String Parameters

The NeonDB connection string includes important SSL parameters:
- `sslmode=require`: Enforces SSL encryption for all connections
- `channel_binding=require`: Adds an additional layer of security

## Installation

1. **Install Dependencies:**
   ```bash
   cd web_todo_app/backend
   pip install -r requirements.txt
   ```

2. **Set Environment Variable:**
   ```bash
   export DATABASE_URL="your-neondb-connection-string"
   ```

3. **Initialize Database Tables:**
   ```bash
   python -c "from src.database import create_db_and_tables; create_db_and_tables()"
   ```

## Data Migration

If you have existing data in SQLite that needs to be migrated to NeonDB:

### Step 1: Export Data from SQLite
```bash
python migrate_export.py
```
This creates a `tasks_export.json` file with all your tasks.

### Step 2: Run Migration
```bash
export DATABASE_URL="your-neondb-connection-string"
python migrate.py
```

### Step 3: Verify Migration
```bash
python migrate_verify.py
```

## Health Checks

### Check Database Connection
```bash
python health_check.py
```

This will verify:
- Database connectivity
- SSL configuration
- Connection parameters

## Running the Application

### Start the Backend Server
```bash
cd web_todo_app/backend
export DATABASE_URL="your-neondb-connection-string"
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Start the Frontend
```bash
cd web_todo_app/frontend
npm run dev
```

The frontend will connect to the backend API, which now uses NeonDB for data storage.

## Troubleshooting

### Connection Errors

**Problem:** "Failed to connect to database"
**Solution:**
- Verify your DATABASE_URL is correct
- Check that SSL parameters are included
- Ensure your network allows connections to NeonDB

**Problem:** "SSL connection error"
**Solution:**
- Verify `sslmode=require` is in your connection string
- Check that your NeonDB instance has SSL enabled

### Migration Issues

**Problem:** "No tasks found in SQLite database"
**Solution:** This is normal if you don't have existing data. Skip migration.

**Problem:** "Data integrity verification failed"
**Solution:**
- Check the error messages from `migrate_verify.py`
- Re-run migration if needed
- Verify SQLite database path is correct

## Performance Considerations

The application is configured with optimal connection pooling for NeonDB:
- Pool size: 5 connections
- Max overflow: 10 additional connections
- Connection pre-ping: Enabled (automatic health checks)
- Pool recycle: 300 seconds (prevents stale connections)

These settings ensure:
- Response times under 2 seconds for all operations
- Efficient connection reuse
- Automatic recovery from transient failures

## Security Best Practices

1. **Never commit DATABASE_URL to version control**
   - Use environment variables
   - Add `.env` files to `.gitignore`

2. **Always use SSL connections**
   - The connection string includes `sslmode=require`
   - This encrypts all data in transit

3. **Rotate credentials regularly**
   - Update your NeonDB password periodically
   - Update the DATABASE_URL environment variable

## Monitoring

The application includes logging for database operations:
- Connection establishment
- Query execution
- Error conditions

Check application logs for database-related messages:
```bash
# Logs will show:
# - "Database engine created for PostgreSQL with connection pooling"
# - "Database tables created successfully"
# - Any error messages with details
```

## Switching Between Databases

The application automatically detects the database type from the connection string:

**To use SQLite:**
```bash
unset DATABASE_URL
# or
export DATABASE_URL="sqlite:///./todo_app.db"
```

**To use NeonDB:**
```bash
export DATABASE_URL="postgresql://..."
```

No code changes are required - the application adapts automatically.

## Additional Resources

- [NeonDB Documentation](https://neon.tech/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)
