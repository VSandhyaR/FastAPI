from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of book",
                                       max_length=100,
                                       min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "4753da60-df3b-4854-b581-d803423c80d4",
                "title": "Computer Science",
                "author": "VSR",
                "description": "computer programming",
                "rating": 90

            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of book",
                                       min_length=1,
                                       max_length=100)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(status_code=418,
                        content={"message":
                                 f"why do you want to read {exception.books_to_return }, read more...!"})


@app.post("/book/login/")
async def book_login(book_id: int, username: Optional[str] = Header(None),
                     password: Optional[str] = Header(None)):
    if username == "FastAPIUser" and password == "test1234":
        return BOOKS[book_id]
    return "Invalid User"


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)
    
    if len(BOOKS) < 1:
        create_book_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        new_books = []
        for i in range(books_to_return):
            new_books.append(BOOKS[i])
        return new_books
    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for b in BOOKS:
        if b.id == book_id:
            return b
    raise item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_no_rating_book(book_id: UUID):
    for b in BOOKS:
        if b.id == book_id:
            return b
    raise item_cannot_be_found_exception()


@app.put("/book_id")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for b in BOOKS:
        if b.id == book_id:
            BOOKS[counter] = book
            return BOOKS[counter]
        counter += 1
    raise item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for b in BOOKS:
        if b.id == book_id:
            del BOOKS[counter]
            return f'ID:{book_id} is deleted'
        counter += 1
    raise item_cannot_be_found_exception()


def create_book_no_api():
    book_1 = Book(id="0753da60-df3b-4854-b581-d803423c80d4",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60
                  )
    book_2 = Book(id="1753da60-df3b-4854-b581-d803423c80d4",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=60
                  )
    book_3 = Book(id="2753da60-df3b-4854-b581-d803423c80d4",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=60
                  )
    book_4 = Book(id="3753da60-df3b-4854-b581-d803423c80d4",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=60
                  )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found",
                         headers={"X-Header-Error":
                                  "Nothing to be seen at the UUID"})