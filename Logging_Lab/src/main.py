from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import logging

# Configure logging with both console and file output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s | %(asctime)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('books_api.log'),
        logging.StreamHandler()
    ]
)

# Create a custom logger for the books API
logger = logging.getLogger("books_api")

# Book model using Pydantic
class Book(BaseModel):
    id: str
    title: str
    author: str
    price: float
    pages: int  # DIFFERENT: Added pages field

# Update model
class BookUpdate(BaseModel):
    title: str
    author: str
    price: float
    pages: int

# Initialize FastAPI app
app = FastAPI(title="Books API", version="1.0.0")

books = [
    Book(id="1", title="The Great Gatsby", author="F. Scott Fitzgerald", price=12.99, pages=180),
    Book(id="2", title="1984", author="George Orwell", price=14.99, pages=328),
    Book(id="3", title="To Kill a Mockingbird", author="Harper Lee", price=13.99, pages=281),
]

logger.info("Books API initialized with %d books", len(books))

# GET /books - Get all books
@app.get("/books", response_model=List[Book])
async def get_books():
    """Get all books"""
    logger.debug("Retrieving all books from database")
    logger.info("GET /books - Returning %d books", len(books))
    return books

# POST /books - Create a new book
@app.post("/books", response_model=Book, status_code=201)
async def create_book(book: Book):
    """Add a new book"""
    logger.debug("Processing new book addition: %s", book.dict())
    
    # DIFFERENT: Check for unrealistic page count
    if book.pages > 2000:
        logger.warning("Unusually high page count detected: %d pages for book '%s'", 
                      book.pages, book.title)
    
    # Check for duplicate ID
    for existing_book in books:
        if existing_book.id == book.id:
            logger.warning("Duplicate book ID detected: %s. Replacing existing entry.", book.id)
    
    books.append(book)
    logger.info("POST /books - Successfully added: '%s' by %s", book.title, book.author)
    return book

# GET /books/{id} - Get book by ID
@app.get("/books/{id}", response_model=Book)
async def get_book_by_id(id: str):
    """Get a specific book by ID"""
    logger.debug("Searching for book with ID: %s", id)
    
    for book in books:
        if book.id == id:
            logger.info("GET /books/%s - Book found: '%s'", id, book.title)
            return book
    
    logger.error("GET /books/%s - Book not found in database", id)
    raise HTTPException(status_code=404, detail="book not found")

# PUT /books/{id} - Update an existing book
@app.put("/books/{id}", response_model=Book)
async def update_book(id: str, updated_book: BookUpdate):
    """Update an existing book"""
    logger.debug("Attempting to update book with ID: %s", id)
    
    for i, book in enumerate(books):
        if book.id == id:
            old_price = book.price
            new_price = updated_book.price
            
            # DIFFERENT: Check for price drops (clearance warning)
            if new_price < old_price * 0.5:
                logger.warning("Significant price drop for book %s: $%.2f -> $%.2f (possible clearance)", 
                             id, old_price, new_price)
            
            # Update the book fields
            books[i].title = updated_book.title
            books[i].author = updated_book.author
            books[i].price = updated_book.price
            books[i].pages = updated_book.pages
            
            logger.info("PUT /books/%s - Successfully updated: '%s'", id, books[i].title)
            return books[i]
    
    logger.error("PUT /books/%s - Book not found for update", id)
    raise HTTPException(status_code=404, detail="book not found")

# DELETE /books/{id} - Delete a book
@app.delete("/books/{id}")
async def delete_book(id: str):
    """Delete a book by ID"""
    logger.debug("Attempting to delete book with ID: %s", id)
    
    # DIFFERENT: Critical if less than 2 books remain
    if len(books) <= 2:
        logger.critical("CRITICAL: Library collection is critically low! Only %d books remaining.", len(books))
    
    for i, book in enumerate(books):
        if book.id == id:
            deleted_book = books.pop(i)
            logger.info("DELETE /books/%s - Successfully removed: '%s'", id, deleted_book.title)
            return {"message": "book deleted successfully", "title": deleted_book.title}
    
    logger.error("DELETE /books/%s - Book not found for deletion", id)
    raise HTTPException(status_code=404, detail="book not found")

# DIFFERENT: Different function name and error
def calculate_average_price():
    """Test function that demonstrates exception logging"""
    try:
        if books:
            logger.debug("calculate_average_price() called")
            total = sum(book.price for book in books)
            average = total / len(books)
            logger.info("Average book price: $%.2f", average)
        
        # Simulate error
        test_list = [1, 2, 3]
        print(test_list[10])  # IndexError instead of ZeroDivisionError
    except IndexError:
        logger.exception("Exception occurred in calculate_average_price() function")

# Main entry point
if __name__ == "__main__":
    logger.info("Starting Books API server on http://0.0.0.0:8080")
    calculate_average_price()
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")