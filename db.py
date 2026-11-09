"""
db.py — Database Configuration

This module handles loading the database connection URL from the environment.
It uses python-dotenv to read values from the .env file so that secrets
(like the database password) are never hard-coded in source code.

The resulting SQL_URL string is imported by other modules (e.g. SQLAlchemy
engine setup) to establish a connection to the PostgreSQL database.
"""

import os  # Used to read environment variables at runtime

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Reads the .env file and injects its values into os.environ


# Load all key=value pairs from .env into the process environment.
# Must be called before any os.getenv() so the values are available.
load_dotenv()

# Retrieve the database connection URL from the environment.
# Storing the URL here (rather than inline everywhere) gives a single place
# to change it if the database host or credentials ever change.
SQL_URL = os.getenv(key="SQL_URL")

engine = create_engine(
    SQL_URL
)  # Placeholder for the SQLAlchemy engine object, initialized later
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()  # Base class for all ORM models; used to register tables


def get_db():
    """
    Dependency function for FastAPI routes.

    Yields a database session that can be used to query or modify the database.
    The session is automatically closed after the request is completed.

    Usage:
        from fastapi import Depends
        from db import get_db

        @app.get("/books")
        def read_books(db: Session = Depends(get_db)):
            return db.query(Book).all()
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use


def create_tables():
    """
    Creates all tables defined in the ORM models.

    This function uses SQLAlchemy's metadata to create the tables in the
    database if they do not already exist. It should be called once at
    application startup to ensure the database schema is initialized.
    """
    base.metadata.create_all(bind=engine)  # Create tables based on registered models


if __name__ == "__main__":
    # If this script is run directly, create the database tables.
    # This is useful for initial setup or testing.
    create_tables()
    print("Database tables created successfully.")
