# operations.py

# 2. Data Storage
# Genres Tuple set of valid categories
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Thriller", "Fantasy")

# Books Dictionary: ISBN (string) -> Book Details (dictionary)
books = {}

# Members List: List of Member Details (dictionaries)
members = []


#function to find a member's index by member_id
def _find_member_index(member_id):
    """Finds the index of a member in the members list by their member_id."""
    for i, member in enumerate(members):
        if member["member_id"] == member_id:
            return i
    return -1


#function to validate genre
def _is_valid_genre(genre):
    """Checks if a genre string is present in the global GENRES tuple (case-insensitive)."""
    return genre.strip().title() in GENRES


# 3. Core Functionality (CRUD Operations)

#Create

def add_book(isbn, title, author, genre, total_copies):
    """
    Adds a new book to the books dictionary if the ISBN is unique and the genre is valid.

    :param isbn: Unique identifier for the book (string).
    :param title: Title of the book (string).
    :param author: Author of the book (string).
    :param genre: Genre of the book (string). Must be in GENRES.
    :param total_copies: Total number of copies available (integer).
    :return: True if successful, False otherwise (ISBN exists or genre is invalid).
    """
    if isbn in books:
        print(f"Error: Book with ISBN {isbn} already exists.")
        return False

    if not _is_valid_genre(genre):
        print(f"Error: Invalid genre '{genre}'. Valid genres are {', '.join(GENRES)}.")
        return False

    if not isinstance(total_copies, int) or total_copies < 1:
        print("Error: Total copies must be a positive integer.")
        return False

    books[isbn] = {
        "title": title.strip(),
        "author": author.strip(),
        "genre": genre.strip().title(),
        "total_copies": total_copies,
    }
    return True


def add_member(member_id, name, email):
    """
    Adds a new member to the members list if the member_id is unique.
    Initializes borrowed_books as an empty list.

    :param member_id: Unique identifier for the member (string).
    :param name: Name of the member (string).
    :param email: Email of the member (string).
    :return: True if successful, False otherwise (member_id exists).
    """
    if _find_member_index(member_id) != -1:
        print(f"Error: Member with ID {member_id} already exists.")
        return False

    new_member = {
        "member_id": member_id.strip(),
        "name": name.strip(),
        "email": email.strip(),
        "borrowed_books": [],
    }
    members.append(new_member)
    return True


## Read

def search_books(query, by="title"):
    """
    Searches books by title or author (case-insensitive, partial matches).

    :param query: Search string (string).
    :param by: Field to search ('title' or 'author'). Default is 'title'.
    :return: A list of matching book dictionaries.
    """
    matching_books = []
    query = query.strip().lower()
    search_key = by.lower()

    if search_key not in ["title", "author"]:
        print(f"Warning: Invalid search field '{by}'. Searching by 'title' instead.")
        search_key = "title"

    for isbn, book in books.items():
        if query in book.get(search_key, "").lower():
            # Include ISBN in the returned dictionary for easy reference
            book_with_isbn = {"isbn": isbn}
            book_with_isbn.update(book)
            matching_books.append(book_with_isbn)

    return matching_books


#Update

def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """
    Updates specified fields of a book if it exists and the genre (if provided) is valid.

    :param isbn: ISBN of the book to update (string).
    :param title: New title (string, optional).
    :param author: New author (string, optional).
    :param genre: New genre (string, optional).
    :param total_copies: New total number of copies (integer, optional).
    :return: True if successful, False otherwise (book not found, or invalid genre/copies).
    """
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    book = books[isbn]

    if title is not None:
        book["title"] = title.strip()
    if author is not None:
        book["author"] = author.strip()
    if genre is not None:
        if _is_valid_genre(genre):
            book["genre"] = genre.strip().title()
        else:
            print(f"Error: Invalid genre '{genre}'. Update failed.")
            return False
    if total_copies is not None:
        if not isinstance(total_copies, int) or total_copies < 0:
            print("Error: Total copies must be a non-negative integer. Update failed.")
            return False
        book["total_copies"] = total_copies

    return True


def update_member(member_id, name=None, email=None):
    """
    Updates specified fields of a member if they exist.

    :param member_id: ID of the member to update (string).
    :param name: New name (string, optional).
    :param email: New email (string, optional).
    :return: True if successful, False otherwise (member not found).
    """
    index = _find_member_index(member_id)
    if index == -1:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    member = members[index]
    if name is not None:
        member["name"] = name.strip()
    if email is not None:
        member["email"] = email.strip()

    return True


#Delete

def delete_book(isbn):
    """
    Removes a book from the books dictionary if it exists and has no borrowed copies.

    :param isbn: ISBN of the book to delete (string).
    :return: True if successful, False otherwise (book not found or has borrowed copies).
    """
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    # Check for borrowed copies
    # We assume 'total_copies' is the currently available copies, and we need to check if ANY member has borrowed it.
    # The requirement is "total_copies equals the original number of copies".
    # Since we don't store the original number, we check if total_copies is less than the max number of times it was borrowed (which is tricky).
    # A simpler, and more robust check, is to see if any *member* currently holds this book.

    for member in members:
        if isbn in member["borrowed_books"]:
            print(f"Error: Cannot delete book {isbn}. It is currently borrowed by at least one member.")
            return False

    # A simpler check based on the prompt's ambiguity:
    # If a book is borrowed, its total_copies will be less than the initial quantity.
    # To properly enforce "no borrowed copies", we must check the members' list.

    # If no member has it, delete it.
    del books[isbn]
    return True


def delete_member(member_id):
    """
    Removes a member from the members list if they exist and have no borrowed books.

    :param member_id: ID of the member to delete (string).
    :return: True if successful, False otherwise (member not found or has borrowed books).
    """
    index = _find_member_index(member_id)
    if index == -1:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    member = members[index]
    if member["borrowed_books"]:
        print(
            f"Error: Cannot delete member {member_id}. They currently have {len(member['borrowed_books'])} book(s) borrowed.")
        return False

    # If no borrowed books, delete the member by index
    members.pop(index)
    return True


## Borrow/Return

def borrow_book(isbn, member_id):
    """
    Handles the borrowing of a book by a member. Checks for availability and loan limits.

    :param isbn: ISBN of the book to borrow (string).
    :param member_id: ID of the member borrowing the book (string).
    :return: True if successful, False otherwise (e.g., book/member not found, unavailable, or loan limit exceeded).
    """
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    book = books[isbn]

    member_index = _find_member_index(member_id)
    if member_index == -1:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    member = members[member_index]

    if book["total_copies"] <= 0:
        print(f"Error: Book '{book['title']}' is currently unavailable (0 copies).")
        return False

    if len(member["borrowed_books"]) >= 3:
        print(f"Error: Member {member_id} has reached the loan limit (3 books).")
        return False

    if isbn in member["borrowed_books"]:
        # Prevent borrowing the same copy multiple times
        print(f"Error: Member {member_id} has already borrowed book {isbn}.")
        return False

    # Valid: Decrement copies and add ISBN to member's list
    book["total_copies"] -= 1
    member["borrowed_books"].append(isbn)
    return True


def return_book(isbn, member_id):
    """
    Handles the returning of a book by a member.

    :param isbn: ISBN of the book to return (string).
    :param member_id: ID of the member returning the book (string).
    :return: True if successful, False otherwise (e.g., book/member not found, or book wasn't borrowed by the member).
    """
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    member_index = _find_member_index(member_id)
    if member_index == -1:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    member = members[member_index]

    if isbn not in member["borrowed_books"]:
        print(f"Error: Book {isbn} was not borrowed by member {member_id}.")
        return False

    # Valid: Increment copies and remove ISBN from member's list
    books[isbn]["total_copies"] += 1
    member["borrowed_books"].remove(isbn)
    return True