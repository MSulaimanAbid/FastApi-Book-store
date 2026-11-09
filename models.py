"""
models.py - SQLAlchemy ORM Models

Defines the database table structure as Python classes.
SQLAlchemy maps each class to a table and each attribute to a column,
so we can work with rows as plain Python objects instead of raw SQL.
"""

# Import column types needed to describe the shape of each database field
from sqlalchemy import Column, Integer, String

# Base is SQLAlchemy's declarative base - every model must inherit from it
# so SQLAlchemy can register the table and manage it automatically
from db import base


class Book(base):
    """
    Represents the "books" table in the database.

    Each instance of Book maps to one row in the table.
    SQLAlchemy uses this class to create the table schema and to
    read/write book records without writing raw SQL.

    Columns:
        id          - int : Auto-incrementing primary key, uniquely identifies each book.
        title       - str : Title of the book. Indexed for fast title-based lookups.
        description - str : A short description or blurb about the book.
        author      - str : Name of the author. Indexed for fast author-based filtering.
        year        - int : Publication year. Indexed for fast year-based filtering.
    """

    __tablename__ = "books"  # The actual table name in the PostgreSQL database

    id = Column(
        Integer, primary_key=True, index=True
    )  # Unique row identifier; auto-assigned by the DB
    title = Column(
        String, index=True
    )  # Book title; indexed so searches by title are fast
    description = Column(
        String
    )  # Optional description; not indexed as it is less commonly queried
    author = Column(String, index=True)  # Author name; indexed for filtering by author
    year = Column(
        Integer, index=True
    )  # Publication year; indexed for date-range queries
