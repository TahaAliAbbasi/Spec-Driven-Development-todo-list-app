"""
Database connection health check utility for NeonDB.

This module provides health check functionality to verify that the application
can successfully connect to the NeonDB PostgreSQL database.
"""

import os
from sqlalchemy import text, create_engine
from sqlalchemy.exc import OperationalError, DatabaseError
from typing import Dict, Any


def check_database_connection(database_url: str = None) -> Dict[str, Any]:
    """
    Check if the database connection is healthy.

    Args:
        database_url: PostgreSQL connection string (defaults to DATABASE_URL env var)

    Returns:
        Dictionary with health check results:
        - status: "healthy" or "unhealthy"
        - database_type: "postgresql" or "sqlite"
        - message: Description of the health check result
        - error: Error message if connection failed (optional)
    """
    if not database_url:
        database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    result = {
        "status": "unhealthy",
        "database_type": "postgresql" if database_url.startswith("postgresql") else "sqlite",
        "message": "",
        "error": None
    }

    try:
        # Create engine with minimal configuration for health check
        engine = create_engine(database_url, pool_pre_ping=True)

        # Test connection with a simple query
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        result["status"] = "healthy"
        result["message"] = f"Successfully connected to {result['database_type']} database"

    except OperationalError as e:
        result["error"] = f"Operational error: {str(e)}"
        result["message"] = "Failed to connect to database - check connection string and network"

    except DatabaseError as e:
        result["error"] = f"Database error: {str(e)}"
        result["message"] = "Database error occurred during health check"

    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        result["message"] = "Unexpected error during health check"

    return result


def check_neondb_ssl_connection(database_url: str = None) -> Dict[str, Any]:
    """
    Verify that SSL connection parameters are properly configured for NeonDB.

    Args:
        database_url: PostgreSQL connection string

    Returns:
        Dictionary with SSL check results
    """
    if not database_url:
        database_url = os.getenv("DATABASE_URL")

    result = {
        "ssl_enabled": False,
        "ssl_mode": None,
        "channel_binding": None,
        "message": ""
    }

    if not database_url or not database_url.startswith("postgresql"):
        result["message"] = "Not a PostgreSQL connection"
        return result

    # Check for SSL parameters in connection string
    if "sslmode=" in database_url:
        result["ssl_enabled"] = True
        # Extract sslmode value
        for param in database_url.split("?")[-1].split("&"):
            if param.startswith("sslmode="):
                result["ssl_mode"] = param.split("=")[1]
            elif param.startswith("channel_binding="):
                result["channel_binding"] = param.split("=")[1]

        if result["ssl_mode"] == "require":
            result["message"] = "SSL connection properly configured"
        else:
            result["message"] = f"SSL mode is '{result['ssl_mode']}' (recommend 'require')"
    else:
        result["message"] = "SSL not configured in connection string"

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Database Connection Health Check")
    print("=" * 60)

    # Check database connection
    health = check_database_connection()
    print(f"\nStatus: {health['status'].upper()}")
    print(f"Database Type: {health['database_type']}")
    print(f"Message: {health['message']}")
    if health['error']:
        print(f"Error: {health['error']}")

    # Check SSL configuration for PostgreSQL
    if health['database_type'] == 'postgresql':
        print("\n" + "=" * 60)
        print("SSL Configuration Check")
        print("=" * 60)
        ssl_check = check_neondb_ssl_connection()
        print(f"\nSSL Enabled: {ssl_check['ssl_enabled']}")
        if ssl_check['ssl_enabled']:
            print(f"SSL Mode: {ssl_check['ssl_mode']}")
            print(f"Channel Binding: {ssl_check['channel_binding']}")
        print(f"Message: {ssl_check['message']}")

    print("\n" + "=" * 60)
