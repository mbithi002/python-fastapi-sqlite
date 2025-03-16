from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Author Models
class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    books: List['BookResponse'] = []

    class Config:
        from_attributes = True

# Book Models
class BookBase(BaseModel):
    title: str
    publication_date: date
    author_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    author: Optional['AuthorResponse'] = None
    loans: List['LoanResponse'] = []

    class Config:
        from_attributes = True

# Borrower Models
class BorrowerBase(BaseModel):
    name: str

class BorrowerCreate(BorrowerBase):
    pass

class BorrowerResponse(BorrowerBase):
    id: int
    loans: List['LoanResponse'] = []

    class Config:
        from_attributes = True

# Loan Models
class LoanBase(BaseModel):
    book_id: int
    borrower_id: int
    return_date: date

class LoanCreate(LoanBase):
    pass

class LoanResponse(LoanBase):
    id: int
    book: Optional['BookResponse'] = None
    borrower: Optional['BorrowerResponse'] = None

    class Config:
        from_attributes = True

# Resolve forward references
AuthorResponse.model_rebuild()
BookResponse.model_rebuild()
BorrowerResponse.model_rebuild()
LoanResponse.model_rebuild()