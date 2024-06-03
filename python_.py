# Python (FastAPI)
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.testclient import TestClient

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: str
    price: float

books = []

@app.get("/books")
def get_books():
    return {"books": books}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return {"book": book}
    return {"message": "Book not found"}

@app.get("/books/title/{book_title}")
def get_books_by_title(book_title: str):
    booksToReturn = [book for book in books if book.title == book_title]
    return {"books": booksToReturn}

@app.get("/books/author/{book_author}")
def get_books_by_author(book_author: str):
    booksToReturn = [book for book in books if book.author == book_author]
    return {"books": booksToReturn}

@app.get("/books/published_date/{book_published_date}")
def get_books_by_date(book_published_date: str):
    booksToReturn = [book for book in books if book.published_date == book_published_date]
    return {"books": booksToReturn}

@app.get("/books/price/{book_price}")
def get_books_by_price(book_price: float):
    booksToReturn = [book for book in books if book.price == book_price]
    return {"books": booksToReturn}

@app.post("/books")
def create_book(book: Book):
    books.append(book)
    return {"message": "Book added successfully"}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    for b in books:
        if b.id == book_id:
            b.title = book.title
            b.author = book.author
            b.published_date = book.published_date
            b.price = book.price
            break
    else:
        return {"message": "Book not found"}
    return {"message": "Book updated successfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            del books[i]
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}

client = TestClient(app)

def test_create_book():
    response = client.post("/books", json={"id": 1, "title": "Book 1", "author": "Author 1", "published_date": "2022-01-01", "price": 9.99})
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully"}

def test_get_book():
    response = client.get("/books/1")
    assert response.status_code == 200

def test_update_book():
    response = client.put("/books/1", json={"id": 1, "title": "Updated Book 1", "author": "Updated Author 1", "published_date": "2022-01-02", "price": 19.99})
    assert response.status_code == 200
    assert response.json() == {"message": "Book updated successfully"}

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200

def test_get_books_by_title():
    response = client.get("/books/title/Book 1")
    assert response.status_code == 200

def test_get_books_by_author():
    response = client.get("/books/author/Author 1")
    assert response.status_code == 200

def test_get_books_by_date():
    response = client.get("/books/published_date/2022-01-01")
    assert response.status_code == 200

def test_get_books_by_price():
    response = client.get("/books/price/19.99")
    assert response.status_code == 200
