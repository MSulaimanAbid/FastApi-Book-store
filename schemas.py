"""
schemas.py - Pydantic Schemas (Request / Response Models)

Pydantic schemas define the shape of data coming IN to the API (requests)
and going OUT of the API (responses). They handle validation automatically —
if a client sends the wrong type, FastAPI rejects it before it ever hits our code.

These schemas are separate from the SQLAlchemy models in models.py:
- models.py  → describes the database table structure
- schemas.py → describes the data shape for the API layer
"""

# BaseModel is the foundation for all Pydantic schemas.
# Any class that inherits from it gets automatic type validation and serialization.
from pydantic import BaseModel


class BookBase(BaseModel):
    """
    Shared base schema that holds all the core fields of a book.

    Other schemas (BookCreate, Book) inherit from this to avoid repeating
    the same field definitions in multiple places.

    Fields:
        id          - int : Unique identifier of the book.
        title       - str : Title of the book.
        description - str : Short description or blurb about the book.
        author      - str : Name of the book's author.
        year        - int : Year the book was published.
    """

    id: int
    title: str
    description: str
    author: str
    year: int


class BookCreate(BookBase):
    """
    Schema used when a client sends a POST request to create a new book.

    Currently empty (pass) — fields will be added here when the create
    endpoint is implemented. Keeping it as a separate class means we can
    add or remove fields for creation independently of the base schema
    (e.g. exclude 'id' since the DB assigns it automatically).
    """


class Book(BookBase):
    """
    Schema used for API responses that return a book object.

    Inherits all fields from BookBase and adds ORM compatibility so
    SQLAlchemy model instances can be returned directly from route handlers
    without manually converting them to dicts.

    Why orm_mode / from_attributes:
        By default Pydantic only reads data from plain dicts.
        orm_mode = True  tells Pydantic to also read attributes from ORM objects.
        from_attributes = True is the Pydantic v2 equivalent of orm_mode.
        Both are set here to support Pydantic v1 and v2 simultaneously.
    """

    id: int

    class Config:
        orm_mode = True  # Pydantic v1: allow reading from SQLAlchemy model attributes
        from_attributes = True  # Pydantic v2: same purpose, new name
