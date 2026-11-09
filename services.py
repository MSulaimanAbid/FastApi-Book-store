"""
services.py - Book CRUD Service Functions

Contains all the database operations (Create, Read, Update, Delete) for books.
Keeping these functions here, separate from the route handlers, means the
business logic can be tested and reused independently of FastAPI routing.

Each function receives a SQLAlchemy Session (db) so the caller (the route
handler) controls when the session is opened and closed - this follows the
dependency-injection pattern used by FastAPI.
"""

# BookCreate schema is used to validate and carry incoming book data
# Session is the SQLAlchemy database session type used for all DB operations
from sqlalchemy.orm import Session

# Book is the ORM model that maps to the "books" table
from models import Book
from schemas import BookCreate


def create_book(db: Session, data: BookCreate):
    """
    Insert a new book record into the database.

    Args:
        db   (Session)    : Active SQLAlchemy database session.
        data (BookCreate) : Validated book data from the request body.

    Returns:
        Book : The newly created Book ORM instance, refreshed from the DB
               so auto-generated fields (e.g. id) are populated.

    How it works:
        1. Convert the Pydantic schema to a dict and unpack it into a Book model instance.
        2. Stage the new row with db.add().
        3. Persist it to the DB with db.commit().
        4. Refresh the instance so the returned object reflects the DB state (e.g. auto id).
    """

    # Unpack the validated Pydantic data into a SQLAlchemy Book instance
    book_instance = Book(**data.model_dump())

    db.add(book_instance)  # Stage the new record - not yet written to DB
    db.commit()  # Write the staged record to the DB permanently
    db.refresh(
        book_instance
    )  # Sync the instance with the DB (loads auto-assigned id etc.)

    return book_instance


def get_book_by_id(db: Session):
    """
    Retrieve all book records from the database.

    Note: The function name says 'by_id' but currently returns all books.
    This may be intentional as a placeholder; do not rename without approval.

    Args:
        db (Session) : Active SQLAlchemy database session.

    Returns:
        list[Book] : A list of all Book ORM instances in the table.
                     Returns an empty list if no books exist.
    """

    # Query every row in the books table and return them as a list
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    """
    Retrieve a single book by its primary key (id).

    Args:
        db      (Session) : Active SQLAlchemy database session.
        book_id (int)     : The primary key of the book to fetch.

    Returns:
        Book | None : The matching Book ORM instance, or None if not found.
    """

    # Filter the books table to the row whose id matches, return first match or None
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book_id: int, data: BookCreate):
    """
    Update an existing book's fields with new data.

    Args:
        db      (Session)    : Active SQLAlchemy database session.
        book_id (int)        : The primary key of the book to update.
        data    (BookCreate) : Validated new data to apply to the book.

    Returns:
        Book | None : The updated Book ORM instance if found, or None if
                      no book with the given id exists.

    How it works:
        1. Fetch the existing book row by id.
        2. If found, loop over all fields in the new data and overwrite each attribute.
        3. Commit the changes and refresh so the returned object is up to date.
    """

    # Find the book to update; returns None if not found
    book_queryset = db.query(Book).filter(Book.id == book_id).first()

    if book_queryset:
        # Loop over each field in the incoming data and apply it to the ORM instance
        for key, value in data.model_dump().items():
            setattr(book_queryset, key, value)  # Dynamically set each attribute by name

        db.commit()  # Persist the updated values to the DB
        db.refresh(book_queryset)  # Sync the instance with the DB after commit

        return book_queryset

    def delete_book(db: Session, book_id: int):
        """
        Delete a book from the database by its primary key.

        Args:
            db      (Session) : Active SQLAlchemy database session.
            book_id (int)     : The primary key of the book to delete.

        Returns:
            Book | None : The deleted Book ORM instance (snapshot before deletion)
                          if found, or None if no book with the given id exists.

        Note: This function is currently indented inside update_book, which means
        it is only defined when update_book is called. This is likely unintentional
        but has NOT been changed per project rules.
        """

        # Find the book to delete; returns None if not found
        book_queryset = db.query(Book).filter(Book.id == book_id).first()

        if book_queryset:
            db.delete(book_queryset)  # Mark the row for deletion
            db.commit()  # Execute the deletion in the DB
            return book_queryset  # Return the deleted instance as confirmation
