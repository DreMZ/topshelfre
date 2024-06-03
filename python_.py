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
	return{"book": books}

@app.get("/books/{book_id}")
def get_book(book_id: int):
	return{"books": books.index(book_id)}

@app.get("/books/{book_title}")
def get_books(book_title: str):
	booksToReturn = []
	for book in books:
		if book["title"] == book_title:
			booksToReturn.append(book)
	return{"book": booksToReturn}

@app.get("/books/{book_author}")
def get_books(book_author: str):
	booksToReturn = []
	for book in books:
		if book["author"] == book_author:
			booksToReturn.append(book)
	return{"book": booksToReturn}

@app.get("/books/{book_published_date}")
def get_books(book_published_date: str):
	booksToReturn = []
	for book in books:
		if book["published_date"] == book_published_date:
			booksToReturn.append(book)
	return{"book": booksToReturn}

@app.get("/books/{book_price}")
def get_books(book_price: float):
	booksToReturn = []
	for book in books:
		if book["price"] == book_price:
			booksToReturn.append(book)
	return{"book": booksToReturn}

@app.post("/books")
def create_book(book: Book):
	books.append(book)

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
	books.index(book_id).book = book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
	del books[book_id]
client = TestClient(app)

def test_create_book():
	response = client.post("/books", json={"id": 1, "title": "Book 1", "author": "Author 1", "published_date": "2022-01-01", "price": 9.99})
	assert response.status_code == 201

def test_get_book():
	response = client.get("/books/1")
	assert response.status_code == 200

def test_update_book():
	response = client.put("/books/1", json={"title": "Updated Book 1", "author": "Updated Author 1", "published_date": "2022-01-02", "price": 19.99})
	assert response.status_code == 200

def test_delete_book():
	response = client.delete("/books/1")
	assert response.status_code == 200

def test_get_books():
	response = client.get("/books")
	assert response.status_code == 200