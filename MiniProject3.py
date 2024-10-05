import json
import os

class Book:
    def __init__(self, title, author, genre, publication_date):
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__publication_date = publication_date
        self.__available = True

    # Getters
    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_genre(self):
        return self.__genre

    def get_publication_date(self):
        return self.__publication_date

    def is_available(self):
        return self.__available

    # Setters
    def set_availability(self, available):
        self.__available = available

    # Display book details
    def display_info(self):
        availability = "Available" if self.__available else "Borrowed"
        return f"Title: {self.__title}, Author: {self.__author}, Genre: {self.__genre}, " \
               f"Publication Date: {self.__publication_date}, Status: {availability}"


class User:
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
        self.__borrowed_books = []

    # Getters
    def get_name(self):
        return self.__name

    def get_library_id(self):
        return self.__library_id

    def get_borrowed_books(self):
        return self.__borrowed_books

    # Borrow a book
    def borrow_book(self, book_title):
        self.__borrowed_books.append(book_title)

    # Return a book
    def return_book(self, book_title):
        if book_title in self.__borrowed_books:
            self.__borrowed_books.remove(book_title)

    # Display user details
    def display_info(self):
        return f"User ID: {self.__library_id}, Name: {self.__name}, Borrowed Books: {', '.join(self.__borrowed_books)}"


class Author:
    def __init__(self, name, biography):
        self.__name = name
        self.__biography = biography

    # Getters
    def get_name(self):
        return self.__name

    def get_biography(self):
        return self.__biography

    # Display author details
    def display_info(self):
        return f"Author: {self.__name}, Biography: {self.__biography}"


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []


def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


class LibraryManagementSystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.authors = []
        self.load_data()

    def load_data(self):
        book_data = load_data('books.json')
        user_data = load_data('users.json')
        author_data = load_data('authors.json')

        for book in book_data:
            self.books.append(Book(book['title'], book['author'], book['genre'], book['publication_date']))
        for user in user_data:
            self.users.append(User(user['name'], user['library_id']))
        for author in author_data:
            self.authors.append(Author(author['name'], author['biography']))

    def save_data(self):
        save_data('books.json', [vars(book) for book in self.books])
        save_data('users.json', [vars(user) for user in self.users])
        save_data('authors.json', [vars(author) for author in self.authors])

    def add_book(self):
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        genre = input("Enter genre: ")
        publication_date = input("Enter publication date: ")
        book = Book(title, author, genre, publication_date)
        self.books.append(book)
        self.save_data()
        print("Book added successfully!")

    def borrow_book(self):
        title = input("Enter the title of the book to borrow: ")
        user_id = input("Enter your user ID: ")
        for book in self.books:
            if book.get_title() == title and book.is_available():
                for user in self.users:
                    if user.get_library_id() == user_id:
                        book.set_availability(False)
                        user.borrow_book(title)
                        self.save_data()
                        print(f"You have borrowed '{title}'.")
                        return
        print("Book not available or user not found.")

    def return_book(self):
        title = input("Enter the title of the book to return: ")
        user_id = input("Enter your user ID: ")
        for user in self.users:
            if user.get_library_id() == user_id:
                user.return_book(title)
                for book in self.books:
                    if book.get_title() == title:
                        book.set_availability(True)
                        self.save_data()
                        print(f"You have returned '{title}'.")
                        return
        print("User not found or book was not borrowed.")

    def search_book(self):
        title = input("Enter the title of the book to search: ")
        for book in self.books:
            if book.get_title().lower() == title.lower():
                print(book.display_info())
                return
        print("Book not found.")

    def display_books(self):
        for book in self.books:
            print(book.display_info())

    def add_user(self):
        name = input("Enter user name: ")
        library_id = input("Enter library ID: ")
        user = User(name, library_id)
        self.users.append(user)
        self.save_data()
        print("User added successfully!")

    def view_user_details(self):
        user_id = input("Enter user ID to view details: ")
        for user in self.users:
            if user.get_library_id() == user_id:
                print(user.display_info())
                return
        print("User not found.")

    def display_users(self):
        for user in self.users:
            print(user.display_info())

    def add_author(self):
        name = input("Enter author name: ")
        biography = input("Enter author biography: ")
        author = Author(name, biography)
        self.authors.append(author)
        self.save_data()
        print("Author added successfully!")

    def view_author_details(self):
        name = input("Enter author name to view details: ")
        for author in self.authors:
            if author.get_name().lower() == name.lower():
                print(author.display_info())
                return
        print("Author not found.")

    def display_authors(self):
        for author in self.authors:
            print(author.display_info())

    def main_menu(self):
        while True:
            print("\nWelcome to the Library Management System!")
            print("1. Book Operations")
            print("2. User Operations")
            print("3. Author Operations")
            print("4. Quit")

            choice = input("Select an option: ")
            if choice == '1':
                self.book_operations()
            elif choice == '2':
                self.user_operations()
            elif choice == '3':
                self.author_operations()
            elif choice == '4':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def book_operations(self):
        while True:
            print("\nBook Operations:")
            print("1. Add a new book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Search for a book")
            print("5. Display all books")
            print("6. Back to Main Menu")

            choice = input("Select an option: ")
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.borrow_book()
            elif choice == '3':
                self.return_book()
            elif choice == '4':
                self.search_book()
            elif choice == '5':
                self.display_books()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def user_operations(self):
        while True:
            print("\nUser Operations:")
            print("1. Add a new user")
            print("2. View user details")
            print("3. Display all users")
            print("4. Back to Main Menu")

            choice = input("Select an option: ")
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.view_user_details()
            elif choice == '3':
                self.display_users()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def author_operations(self):
        while True:
            print("\nAuthor Operations:")
            print("1. Add a new author")
            print("2. View author details")
            print("3. Display all authors")
            print("4. Back to Main Menu")

            choice = input("Select an option: ")
            if choice == '1':
                self.add_author()
            elif choice == '2':
                self.view_author_details()
            elif choice == '3':
                self.display_authors()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    library_system = LibraryManagementSystem()
    library_system.main_menu()
