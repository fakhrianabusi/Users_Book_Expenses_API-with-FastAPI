# TO BE IMPLEMENTED

from fastapi import APIRouter, HTTPException, status, Path
from pydantic import BaseModel
from database import books


router = APIRouter(tags=["Books"])


class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    num_pages: int
    publication_year: int


class BookUpdate(BaseModel):
    title: str | None
    author: str | None
    price: float | None
    num_pages: int | None
    publication_year: int | None


class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    price: float
    num_pages: int
    publication_year: int


@router.get("/books")
def get_all_books():
    return books


@router.get("/books/{book_id}", response_model=BookPublic)
def get_book_by_id(
    book_id: int = Path(..., gt=0, description="Enter The ID of the book"),
):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found!",
    )


@router.post("/books", response_model=BookPublic, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    max_id = max(expense["id"] for expense in books) + 1  # type: ignore
    db_book = book.model_dump()
    db_book["id"] = max_id
    books.append(db_book)
    return db_book


@router.patch("/books/{id}", response_model=BookPublic)
def update_book(id: int, book: BookUpdate):
    for index, item in enumerate(books):
        if item["id"] == id:
            books[index].update(book.model_dump(exclude_none=True))
            return books[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found!"
    )


@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    for index, item in enumerate(books):
        if item["id"] == id:
            del books[index]
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found!"
    )
