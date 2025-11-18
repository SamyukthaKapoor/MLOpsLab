### Logging Lab - Books API
Learning Python logging fundamentals through a FastAPI application that manages a book collection.

#### Setup
Install required dependencies:
```bash
pip install -r requirements.txt
```

#### Running the Application
Navigate to the src folder and start the FastAPI server:
```bash
cd src
python main.py
```

The API will be available at http://localhost:8080

All logs will be displayed in the console and saved to `books_api.log`

#### Testing Different Log Levels

**DEBUG & INFO - Get all books:**
```bash
curl http://localhost:8080/books
```

**WARNING - Add book with unrealistic page count:**
```bash
curl -X POST http://localhost:8080/books \
  -H "Content-Type: application/json" \
  -d '{"id":"4","title":"War and Peace","author":"Leo Tolstoy","price":18.99,"pages":2500}'
```

**WARNING - Update with significant price drop:**
```bash
curl -X PUT http://localhost:8080/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"The Great Gatsby","author":"F. Scott Fitzgerald","price":3.00,"pages":180}'
```

**ERROR - Try to get non-existent book:**
```bash
curl http://localhost:8080/books/999
```

**CRITICAL - Delete books until only 2 or fewer remain:**
```bash
curl -X DELETE http://localhost:8080/books/1
curl -X DELETE http://localhost:8080/books/2
```

**EXCEPTION - Logged automatically on startup** (from `calculate_average_price()` function)

#### Viewing Logs

**Real-time console output:**
Check the terminal where you ran `python main.py`

**View log file:**
```bash
cat books_api.log
```

**Monitor log file in real-time:**
```bash
tail -f books_api.log
```

#### Log Levels Demonstrated
- **DEBUG**: Detailed debugging information (retrieving books, searching operations)
- **INFO**: General informational messages (successful operations, server startup, statistics)
- **WARNING**: Potential issues (unrealistic page counts, significant price drops)
- **ERROR**: Error events (book not found, failed operations)
- **CRITICAL**: Critical situations (library collection critically low)
- **EXCEPTION**: Full traceback of exceptions (IndexError in calculate_average_price)
