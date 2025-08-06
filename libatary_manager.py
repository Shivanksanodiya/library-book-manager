# library_manager.py
import os
import json

class Book:
    def _init_(self, title, author, year, isbn, is_borrowed=False):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "is_borrowed": self.is_borrowed
        }

    @staticmethod
    def from_dict(data):
        return Book(
            data["title"],
            data["author"],
            data["year"],
            data["isbn"],
            data.get("is_borrowed", False)
        )

class LibraryManager:
    def _init_(self, filename="books.txt"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    data = json.load(f)
                    self.books = [Book.from_dict(book) for book in data]
                except json.JSONDecodeError:
                    self.books = []

    def save_books(self):
        with open(self.filename, "w") as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def add_book(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        year = input("Enter year: ")
        isbn = input("Enter ISBN: ")
        book = Book(title, author, year, isbn)
        self.books.append(book)
        self.save_books()
        print("Book added successfully.\n")

    def list_books(self):
        if not self.books:
            print("No books found.\n")
            return
        for i, book in enumerate(self.books, 1):
            status = "Borrowed" if book.is_borrowed else "Available"
            print(f"{i}. {book.title} by {book.author} ({book.year}) [ISBN: {book.isbn}] - {status}")
        print()

    def search_books(self):
        keyword = input("Enter title, author, or year to search: ").lower()
        results = [book for book in self.books if keyword in book.title.lower() or keyword in book.author.lower() or keyword in book.year.lower()]
        if not results:
            print("No matching books found.\n")
        else:
            for i, book in enumerate(results, 1):
                status = "Borrowed" if book.is_borrowed else "Available"
                print(f"{i}. {book.title} by {book.author} ({book.year}) - {status}")
            print()

    def borrow_book(self):
        self.list_books()
        isbn = input("Enter ISBN of the book to borrow: ")
        for book in self.books:
            if book.isbn == isbn:
                if book.is_borrowed:
                    print("Book is already borrowed.\n")
                else:
                    book.is_borrowed = True
                    self.save_books()
                    print("Book borrowed successfully.\n")
                return
        print("Book not found.\n")

    def return_book(self):
        isbn = input("Enter ISBN of the book to return: ")
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_borrowed:
                    print("Book is not currently borrowed.\n")
                else:
                    book.is_borrowed = False
                    self.save_books()
                    print("Book returned successfully.\n")
                return
        print("Book not found.\n")

    def run(self):
        while True:
            print("""
Library Menu:
1. Add New Book
2. List All Books
3. Search for Books
4. Borrow a Book
5. Return a Book
6. Exit
""")
            choice = input("Choose an option (1-6): ")
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.list_books()
            elif choice == "3":
                self.search_books()
            elif choice == "4":
                self.borrow_book()
            elif choice == "5":
                self.return_book()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.\n")

if _name_ == "_main_":
    manager = LibraryManager()
    manager.run()