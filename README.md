# Mini Library Management System (Python)

This is a simple, in-memory library management system implemented in Python. It provides core **CRUD** (Create, Read, Update, Delete) and **Borrow/Return** functionalities for managing a catalog of books and a list of library members.

The system uses Python dictionaries and lists to store data, making it straightforward and easy to understand.

## Project Structure

The system is split into two primary files:

* **`ag_operations.py`**: Contains all the data structures (books, members) and the core business logic functions (add\_book, borrow\_book, search\_books, etc.).
* **`ag_demo.py`**: A demonstration file that imports functions from `operations.py` to showcase the system's usage and features.
* **`ag_tests.py`**: A simple unit test file to ensure the core functionalities and their constraints/edge cases work as expected.

## Setup and Running

Since this is a pure Python project with no external dependencies, setup is straightforward.

1.  **Clone or Download:** Get the project files.
2.  **Run the Demo (Optional):** To see the system in action, run the `demo.py` file:
    ```bash
    python ag_demo.py
    ```
3.  **Run the Tests (Recommended):** To verify all functions work correctly, run the `tests.py` file:
    ```bash
    python ag_tests.py
    ```

## ✨ Core Functionalities

### 1. Data Structures

The system manages two main collections:

* **`GENRES`**: A tuple of valid book categories (e.g., `("Fiction", "Non-Fiction", "Sci-Fi", ...)`).
* **`books`**: A dictionary where the **ISBN** (string) is the key, and the value is a dictionary containing book details: `{"title": "...", "author": "...", "genre": "...", "total_copies": 3}`.
* **`members`**: A list of member dictionaries, where each member has: `{"member_id": "...", "name": "...", "email": "...", "borrowed_books": ["ISBN1", "ISBN2"]}`.

---

### 2. Book Management (CRUD)

| Function | Description | Constraints/Notes |

| **`add_book`** | Adds a new book. | ISBN must be unique. Genre must be in `GENRES`. Total copies must be a positive integer. |
| **`search_books`** | Finds books by **title** (default) or **author**. | Performs a case-insensitive, partial-match search. |
| **`update_book`** | Modifies an existing book's details. | Accepts optional parameters (title, author, genre, total\_copies). New genre must be valid. |
| **`delete_book`** | Removes a book from the catalog. | **Cannot delete** if any member currently has the book borrowed. |

**Example Usage:**

```python
from operations import add_book, search_books

add_book("B001", "The Great Code", "Ada Lovelace", "Sci-Fi", 5)
add_book("B002", "Travels", "Gulliver", "Fiction", 2)

# Search for books with "travel" in the title
found = search_books("travel")
# [{'isbn': 'B002', 'title': 'Travels', 'author': 'Gulliver', ...}]