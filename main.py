from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import BookModel

# Create database tables
Base.metadata.create_all(bind=engine)


class BookCreate(BaseModel):
    """Schema for creating or updating a book."""
    title: str = Field(..., min_length=1, description="The title of the book")
    author: str = Field(..., min_length=1, description="The author of the book")
    rating: float = Field(..., ge=0, le=5, description="The rating of the book (0-5)")
    is_read: bool = Field(default=False, description="Whether the book has been read")
    cover_url: Optional[str] = Field(None, description="URL of the book cover image")
    genre: Optional[str] = Field(None, description="Genre of the book")

class BookResponse(BookCreate):
    """Schema for a book response, including the database ID."""
    id: int


app = FastAPI(
    title="Book Library API",
    description="A robust API for managing a personal library of books.",
    version="1.0.0",
)

# Add CORS Middleware for production readiness
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, summary="Serve Frontend UI")
def serve_ui():
    """Serves the static HTML frontend for the Book Library application."""
    html_path = Path("index.html")
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>UI not found</h1><p>Ensure index.html is in the project folder.</p>"


def get_db():
    """Yields a database session and ensures it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books", response_model=List[BookResponse], summary="List all books")
def list_books(
    author: Optional[str] = Query(None, description="Filter by author name (partial match)"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    max_rating: Optional[float] = Query(None, ge=0, le=5, description="Maximum rating"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of books from the library.
    Optional query parameters can be used to filter the results.
    """
    query = db.query(BookModel)

    if author is not None:
        query = query.filter(BookModel.author.ilike(f"%{author}%"))
    if min_rating is not None:
        query = query.filter(BookModel.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(BookModel.rating <= max_rating)
    if is_read is not None:
        query = query.filter(BookModel.is_read == is_read)

    return query.all()


@app.get("/books/{book_id}", response_model=BookResponse, summary="Get a book by ID")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a single book by its database ID."""
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=BookResponse, status_code=201, summary="Add a new book")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the library."""
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put("/books/{book_id}", response_model=BookResponse, summary="Update an existing book")
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Update all fields of an existing book by its ID."""
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.model_dump().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}", summary="Delete a book")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Remove a book from the library by its ID."""
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully", "id": book_id}
