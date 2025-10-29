# demo.py

from ag_operations import GENRES, books, members, add_book, add_member, search_books, update_book, update_member, \
    delete_book, delete_member, borrow_book, return_book


def print_system_state(header):
    """Prints the current state of books and members with clear formatting."""
    print("\n" + "=" * 50)
    print(f"SYSTEM STATE: {header}")
    print("=" * 50)

    print("\n--- BOOKS CATALOG ---")
    if books:
        for isbn, book in books.items():
            print(
                f"ISBN: {isbn} | Title: {book['title']:<20} | Author: {book['author']:<15} | Copies: {book['total_copies']}")
    else:
        print("The books catalog is empty.")

    print("\n--- MEMBERS LIST ---")
    if members:
        for member in members:
            borrowed_titles = [books[isbn]['title'] for isbn in member['borrowed_books'] if isbn in books]
            print(
                f"ID: {member['member_id']} | Name: {member['name']:<15} | Email: {member['email']:<20} | Borrowed: {', '.join(borrowed_titles) if borrowed_titles else 'None'} ({len(member['borrowed_books'])})")
    else:
        print("The members list is empty.")
    print("-" * 50)


def main_demo():
    print("<<< Mini Library Management System Demo >>>")
    print(f"Initialized with GENRES: {GENRES}")

    # 1. INITIALIZATION: Add Books and Members

    print_system_state("Initial Setup")

    # Add 5 Books
    print("\n--- 1.1 Creating 5 Books ---")
    add_book("B101", "The Alchemist", "Paulo Coelho", "Fiction", 3)
    add_book("B102", "Python Crash Course", "Eric Matthes", "Non-Fiction", 5)
    add_book("B103", "Dune", "Frank Herbert", "Sci-Fi", 2)
    add_book("B104", "The Silent Patient", "Alex Michaelides", "Thriller", 1)
    add_book("B105", "Sapiens", "Yuval Noah Harari", "Biography", 4)
    # Failed create attempt
    add_book("B101", "Duplicate Book", "Test Author", "Fiction", 1)

    # Add 3 Members
    print("\n--- 1.2 Creating 3 Members ---")
    add_member("M001", "Alice Smith", "alice@lib.com")
    add_member("M002", "Bob Johnson", "bob@lib.com")
    add_member("M003", "Charlie Brown", "charlie@lib.com")
    # Failed create attempt
    add_member("M001", "Duplicate Member", "test@lib.com")

    print_system_state("After Initial Creation")

    # 2. READ: Search Operations

    print("\n   2.1 Searching Books by Title ('Python')   ")
    search_results = search_books("Python")
    print(f"Found {len(search_results)} result(s):")
    for book in search_results:
        print(f"  - {book['title']} by {book['author']} (ISBN: {book['isbn']})")

    print("\n--- 2.2 Searching Books by Author ('Frank') ---")
    search_results = search_books("Frank", by="author")
    print(f"Found {len(search_results)} result(s):")
    for book in search_results:
        print(f"  - {book['title']} by {book['author']} (ISBN: {book['isbn']})")

    # --- 3. BORROW/RETURN FUNCTIONALITY ---

    print("\n   3.1 Borrowing Books   ")
    # Alice borrows "The Alchemist" and "Dune"
    borrow_book("B101", "M001")
    borrow_book("B103", "M001")
    # Bob borrows the single copy of "The Silent Patient"
    borrow_book("B104", "M002")
    # Charlie borrows 3 books to hit the limit
    borrow_book("B105", "M003")
    borrow_book("B102", "M003")
    borrow_book("B101", "M003")  # Alice's copy of B101 is available because total_copies was 3

    print_system_state("After Initial Borrowing")

    print("\n--- 3.2 Borrow/Availability Edge Cases ---")
    # Attempt to borrow unavailable book (B104 has 0 copies now)
    borrow_book("B104", "M001")
    # Attempt to borrow when limit is reached (Charlie has 3)
    borrow_book("B103", "M003")

    print("\n   3.3 Returning a Book   ")
    # Alice returns "The Alchemist"
    return_book("B101", "M001")
    # Attempt to return a book not borrowed by the member
    return_book("B102", "M002")

    print_system_state("After Returns and Edge Cases")

    # 4. UPDATE OPERATIONS

    print("\n   4.1 Updating Book (B103) ")
    update_book("B103", genre="Fantasy", total_copies=3)

    print("\n--- 4.2 Updating Member (M002) ---")
    update_member("M002", name="Robert Johnson", email="robert.j@lib.com")
    # Failed update attempt (non-existent ID)
    update_member("M999", name="Fake Name")

    print_system_state("After Update Operations")

    #5. DELETE OPERATIONS

    print("\n--- 5.1 Delete Edge Cases ---")
    # Attempt to delete book B103 (Dune) while it is still borrowed by M001
    delete_book("B103")
    # Attempt to delete member M002 while they have a book borrowed
    delete_member("M002")

    print("\n--- 5.2 Successful Deletion ---")
    # Delete B105, which is not borrowed (Charlie borrowed it but returned it implicitly in the return steps above for other books, but B105 is still borrowed by Charlie. Let's fix that first.)
    # Charlie returns the remaining books: B105, B102, B101
    return_book("B105", "M003")
    return_book("B102", "M003")
    return_book("B101", "M003")

    # Now successfully delete book B105
    delete_book("B105")

    # Now successfully delete member M003
    delete_member("M003")

    print_system_state("After Successful Deletions (B105, M003)")

    print("\n    Demo Complete    ")


if __name__ == "__main__":
    main_demo()