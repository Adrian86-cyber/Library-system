# tests.py

from ag_operations import (
    GENRES, books, members,
    add_book, add_member, search_books,
    update_book, update_member, delete_book,
    delete_member, borrow_book, return_book
)


# function to reset data for clean testing
def reset_data():
    """Clears the global books and members lists for a fresh test run."""
    books.clear()
    members[:] = []
    print("\n--- Data Reset ---")


# Unit Tests

def run_tests():
    print("--- Running Unit Tests ---")

    # TEST 1: Basic Create (add_book) and Constraint (invalid genre)
    reset_data()
    # Success case
    assert add_book("978-0321765723", "The C Programming Language", "Dennis Ritchie", "Non-Fiction",
                    3) == True, "TEST 1.1: Failed to add valid book."
    # Failure case: ISBN exists
    assert add_book("978-0321765723", "Duplicate Book", "Author A", "Fiction",
                    1) == False, "TEST 1.2: Added book with duplicate ISBN."
    # Failure case: Invalid genre
    assert add_book("999-0000000000", "Bad Book", "Author B", "Poetry",
                    1) == False, "TEST 1.3: Added book with invalid genre."
    print(f"TEST 1: Basic Create & Constraint Passed. Current books: {len(books)}")

    # TEST 2: Borrow/Return Functionality (Normal and Limit/Unavailable Edge Cases)
    reset_data()
    # Setup for Test 2
    add_book("B001", "Book One", "Author A", "Fiction", 1)
    add_book("B002", "Book Two", "Author A", "Fiction", 1)
    add_book("B003", "Book Three", "Author A", "Fiction", 1)
    add_book("B004", "Book Four", "Author A", "Fiction", 1)
    add_member("M001", "Max Loaner", "max@loan.com")

    # 2.1: Normal Borrow (Decrements total_copies, adds to member)
    assert borrow_book("B001", "M001") == True, "TEST 2.1: Failed to borrow first book."
    assert books["B001"]["total_copies"] == 0, "TEST 2.1: total_copies did not decrement."
    assert "B001" in members[0]["borrowed_books"], "TEST 2.1: ISBN not added to member's list."

    # 2.2: Unavailable Edge Case (Borrowing when total_copies == 0)
    assert borrow_book("B001", "M001") == False, "TEST 2.2: Borrowed a book with 0 copies."

    # 2.3: Reaching Loan Limit (Borrowing 3 books)
    borrow_book("B002", "M001")
    borrow_book("B003", "M001")
    assert len(members[0]["borrowed_books"]) == 3, "TEST 2.3: Did not reach 3 borrowed books."

    # 2.4: Exceeding 3-loan limit
    assert borrow_book("B004", "M001") == False, "TEST 2.4: Exceeded the 3-loan limit."

    # 2.5: Normal Return (Increments total_copies, removes from member)
    assert return_book("B001", "M001") == True, "TEST 2.5: Failed to return book."
    assert books["B001"]["total_copies"] == 1, "TEST 2.5: total_copies did not increment upon return."
    assert "B001" not in members[0]["borrowed_books"], "TEST 2.5: ISBN was not removed from member's list."

    # 2.6: Returning a non-borrowed book (from an existing member)
    assert return_book("B004", "M001") == False, "TEST 2.6: Returned a book the member never borrowed."
    print("TEST 2: Borrow/Return & Edge Cases Passed.")

    # TEST 3: Update and Search
    reset_data()
    add_book("B999", "Old Title", "Old Author", GENRES[0], 2)

    # Update book title and author
    assert update_book("B999", title="New Title",
                       author="New Author") == True, "TEST 3.1: Failed to update book title/author."
    assert books["B999"]["title"] == "New Title", "TEST 3.1: Title was not updated."

    # Search by updated title (partial match, case-insensitive)
    assert len(search_books("New Title", by="title")) == 1, "TEST 3.2: Search by title failed."
    assert len(search_books("new", by="author")) == 1, "TEST 3.3: Search by author failed (partial match)."

    # Update book copies
    assert update_book("B999", total_copies=5) == True, "TEST 3.4: Failed to update total_copies."
    assert books["B999"]["total_copies"] == 5, "TEST 3.4: total_copies update failed."

    print("TEST 3: Update and Search Passed.")

    # TEST 4: Member CRUD
    reset_data()
    add_member("M002", "Jane Doe", "jane@test.com")

    # Read/check member added
    assert len(members) == 1, "TEST 4.1: Member not added."

    # Update member email
    assert update_member("M002", email="new_jane@test.com") == True, "TEST 4.2: Failed to update member."
    assert members[0]["email"] == "new_jane@test.com", "TEST 4.2: Member email update failed."

    # Delete member (no borrowed books)
    assert delete_member("M002") == True, "TEST 4.3: Failed to delete member with no borrowed books."
    assert len(members) == 0, "TEST 4.3: Member was not removed from list."

    print("TEST 4: Member CRUD Passed.")

    # TEST 5: Delete Edge Cases (Book/Member with borrowed items)
    reset_data()
    add_book("B111", "Loaned Book", "Author L", "Fiction", 1)
    add_member("M111", "Cannot Delete", "delete@no.com")
    borrow_book("B111", "M111")

    # Delete Book (with borrowed copies)
    assert delete_book("B111") == False, "TEST 5.1: Deleted a book that is currently borrowed."

    # Delete Member (with borrowed books)
    assert delete_member("M111") == False, "TEST 5.2: Deleted a member who currently has books borrowed."

    print("TEST 5: Delete Edge Cases Passed.")

    print("\n*** All 5 Unit Tests Passed Successfully! ***")


if __name__ == "__main__":
    run_tests()