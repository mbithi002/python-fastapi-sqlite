# import packages
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import Optional
from pydantic_schemas import AuthorBase, AuthorCreate, AuthorResponse, BookBase, BookCreate, BookResponse, BorrowerBase, BorrowerCreate, BorrowerResponse, LoanBase, LoanCreate, LoanResponse


# initialize application
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(DATABASE_URL, connect_args={ "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Book model
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    loans = relationship("Loan", back_populates="book")

# SQLAlchemy Author model
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("Book", back_populates="author")
    
# SQLAlchemy Borrower model
class Borrower(Base):
    __tablename__ = "borrowers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    loans = relationship("Loan", back_populates="borrower")

# SQLAlchemy Loan model
class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    borrower_id = Column(Integer, ForeignKey("borrowers.id"))
    return_date = Column(Date)
    book = relationship("Book", back_populates="loans")
    borrower = relationship("Borrower", back_populates="loans")

# Build the database
Base.metadata.create_all(bind=engine)

# dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Server's base URL method
@app.get("/")
def index():
    return {
        "message" : "LIBRARY MANAGEMENT SYSTEMS"
    }
    

# CRUD

# CRUD for Books
@app.get("/books/", response_model=list[BookResponse])
def get_books(*, offset: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    books = db.query(Book).offset(offset).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=BookBase)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookBase, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Loop over the key-value pairs in the update payload
    for key, value in book.model_dump().items():
        if value is not None:  # Only update fields that are not None
            setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

# CRUD for Author
@app.get("/authors", response_model=list[AuthorResponse])
def get_author(*, offset: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    authors = db.query(Author).offset(offset).limit(limit).all()
    return authors

@app.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None: 
        raise HTTPException(status_code=404, detail = "Author not found")
    return author

@app.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.put("/authors/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorBase, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None: 
        raise HTTPException(status_code=404, detail="Author not found")
    # Loop over the key-value pairs in the update payload
    for key, value in author.model_dump().items():
        if value is not None: 
            setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}", response_model=AuthorResponse)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return db_author

# CRUD for Borrower

@app.get("/borrowers", response_model=list[BorrowerResponse])
def get_borrower(*, offset: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    borrowers = db.query(Borrower).offset(offset).limit(limit).all()
    return borrowers

@app.get("/borrowers/{borrower_id}", response_model=BorrowerResponse)
def get_borrower_by_id(borrower_id: int, db: Session = Depends(get_db)):
    borrower = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if borrower is None:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return borrower

@app.post("/borrowers/", response_model=BorrowerResponse)
def create_borrower(borrower: BorrowerCreate, db: Session = Depends(get_db)):
    db_borrower = Borrower(**borrower.model_dump())
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    return db_borrower

@app.put("/borrowers/{borrower_id}", response_model=BorrowerResponse)
def update_borrower(borrower_id: int, borrower: BorrowerBase, db: Session = Depends(get_db)):
    db_borrower = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if db_borrower is None:
        raise HTTPException(status_code=404, detail="Borrower not found")
    # Loop over the key-value pairs in the update payload
    for key, value in borrower.model_dump().items():
        if value is not None:
            setattr(db_borrower, key, value)
    
    db.commit()
    db.refresh(db_borrower)
    return db_borrower

@app.delete("/borrowers/{borrower_id}", response_model=BorrowerResponse)
def delete_borrower(borrower_id: int, db: Session = Depends(get_db)):
    db_borrower = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if db_borrower is None:
        raise HTTPException(status_code=404, detail="Borrower not found")
    
    db.delete(db_borrower)
    db.commit()
    return db_borrower

# CRUD fro Loan
@app.get("/loans", response_model=list[LoanResponse])
def get_loan(*, offset: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    loans = db.query(Loan).offset(offset).limit(limit).all()
    return loans

@app.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.post("/loans/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@app.put("/loans/{loan_id}", response_model=LoanResponse)
def update_loan(loan_id: int, loan: LoanBase, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    # Loop over the key-value pairs in the update payload
    for key, value in loan.model_dump().items():
        if value is not None:
            setattr(db_loan, key, value)
    
    db.commit()
    db.refetch(db_loan)
    return db_loan

@app.delete("/loans/{loan_id}", response_model=LoanResponse)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    db.delete(db_loan)
    db.commit()
    return db_loan


# Filtered Query
@app.get("/books/", response_model=list[BookResponse])
def read_books(
    author_id: int = Query(None, description="Filter by author ID"),
    available: bool = Query(None, description="Filter by availability"),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    if available is not None:
        if available:
            query = query.filter(~Book.id.in_(db.query(Loan.book_id)))
        else:
            query = query.filter(Book.id.in_(db.query(Loan.book_id)))
    return query.all()