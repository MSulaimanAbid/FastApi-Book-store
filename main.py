"""
main.py - FastAPI Application Entry Point

This is where the FastAPI app is created and all HTTP route handlers are defined.
Each route handler receives a request, delegates the actual DB work to services.py,
and returns a response shaped by the schemas in schemas.py.

Separation of concerns:
    main.py     -> HTTP layer: routes, status codes, HTTP errors
    services.py -> Business/data layer: DB queries and mutations
    schemas.py  -> Validation layer: request/response shape
    models.py   -> DB layer: table structure
"""

# Depends     - FastAPI's dependency injection system (used to inject the DB session)
# FastAPI     - The main application class
# HTTPException - Used to return HTTP error responses (e.g. 404 Not Found)
from fastapi import Depends, FastAPI, HTTPException

# Session is the SQLAlchemy session type; used for type hints on the db parameter
from sqlalchemy.orm import Session

import schemas  # Pydantic schemas for request validation and response serialization
import services  # Service functions that contain the actual DB logic
from db import create_tables, get_db

# Dependency that opens and yields a DB session per request
create_tables()  # Ensure the database tables are created at startup
# Create the FastAPI application instance.
# This object is what Uvicorn runs; it holds all routes and middleware.
app = FastAPI()


@app.get("/books", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)):
    """
    GET /books - Retrieve all books.

    Args:
        db (Session) : DB session injected automatically by FastAPI via Depends(get_db).

    Returns:
        list[schemas.Book] : A list of all books in the database, serialized
                             using the Book schema. Returns an empty list if none exist.
    """
    # Delegate to the service layer to fetch all book records
    return services.get_book_by_id(db)


@app.get("/books/{id}", response_model=schemas.Book)
async def get_book_by_id(id: int, db: Session = Depends(get_db)):
    """
    GET /books/{id} - Retrieve a single book by its id.

    Args:
        id (int)     : The book's primary key, extracted from the URL path.
        db (Session) : DB session injected automatically by FastAPI via Depends(get_db).

    Returns:
        schemas.Book : The matching book serialized using the Book schema.

    Raises:
        HTTPException (404) : If no book exists with the given id.
    """
    # Ask the service layer to look up the book; returns None if not found
    book_queryset = services.get_book(db, id)

    if book_queryset:
        return book_queryset  # Found - return the book as a response

    # Not found - raise a 404 so the client knows the id doesn't exist
    raise HTTPException(status_code=404, detail="Book not found by the given id.")


@app.post("/books", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    POST /books - Create a new book.

    Args:
        book (schemas.BookCreate) : Request body, validated against the BookCreate schema.
        db   (Session)            : DB session injected automatically by FastAPI via Depends(get_db).

    Returns:
        schemas.Book : The newly created book (including its auto-assigned id),
                       serialized using the Book schema.
    """
    # Pass the validated request data straight to the service layer to insert into the DB
    return services.create_book(db, book)


@app.put("/books/{id}", response_model=schemas.Book)
async def update_book(id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    PUT /books/{id} - Update an existing book by its id.

    Args:
        id   (int)               : The book's primary key, extracted from the URL path.
        book (schemas.BookUpdate): Request body with the new values, validated by BookUpdate.
        db   (Session)           : DB session injected automatically by FastAPI via Depends(get_db).

    Returns:
        schemas.Book : The updated book serialized using the Book schema.

    Raises:
        HTTPException (404) : If no book exists with the given id.
    """
    # Attempt the update; service returns None if the book id doesn't exist
    db_update = services.update_book(db, id, book)

    if not db_update:
        # Book not found - tell the client with a 404
        raise HTTPException(status_code=404, detail="Book not found")

    return db_update  # Update succeeded - return the updated book


@app.delete("/books/{id}", response_model=schemas.Book)
async def delete_book(id: int, db: Session = Depends(get_db)):
    """
    DELETE /books/{id} - Delete a book by its id.

    Args:
        id (int)     : The book's primary key, extracted from the URL path.
        db (Session) : DB session injected automatically by FastAPI via Depends(get_db).

    Returns:
        schemas.Book : The deleted book's data (snapshot before deletion),
                       serialized using the Book schema.

    Raises:
        HTTPException (404) : If no book exists with the given id.
    """
    # Attempt the deletion; service returns the deleted record or None if not found
    delete_entry = services.delete_book(db, id)

    if delete_entry:
        return (
            delete_entry  # Deletion succeeded - return the deleted book as confirmation
        )

    # Book not found - tell the client with a 404
    raise HTTPException(status_code=404, detail="Book not found")
