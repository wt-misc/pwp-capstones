class User(object):
    def __init__(self, name, email):
        self.email = email
        self.name = name
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        print("Email address for user {user} has been changed from {old} to {new}".format
            (user=self.name, old=self.email, new=address))
        self.email = address

    def __repr__(self):
        return ("User {user}, email: {email}, books read: {num}".format
            (user=self.name, email=self.email, num=len(self.books)))

    def __eq__(self, other_user):
        if (self.email == other_user.email) and (self.name == other_user.name):
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0
        count = 0
        for rating in self.books.values():
            if (type(rating) == int) and (rating >= 0) and (rating <= 4):
                total += rating
                count += 1
        return total / count
                    

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        print("ISBN for title \"{title}\" has been changed from {old} to {new}".format
            (title=self.title, old=self.isbn, new=new_isbn))

    def add_rating(self, rating):
        if (type(rating) != int) or (rating < 0) or (rating > 4):
            print("Invalid Rating")
        else:
            self.ratings.append(rating)

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def get_average_rating(self):
        total = 0
        for rating in self.ratings:
            total += rating
        return total / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return self.title



class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return ("{title}, a {level} manual on {subject}".format
            (title=self.title, level=self.level, subject=self.subject))

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email, None)
        if not user:
            print("No user with email {email}".format(email=email))
        else:
            user.read_book(book, rating)
            if rating:
                book.add_rating(rating)
            num_users = self.books.get(book, 0)
            self.books[book] = num_users + 1

    def add_user(self, name, email, user_books=None):
        user = User(name, email)
        self.users[email] = user
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)
    
    def print_catalog(self):
        print("== Book Catalog: ==")
        for book, num_users in self.books.items():
            print(" {title} (ISBN: {isbn}, readers: {num_users})".format
                (title=book.title, isbn=book.isbn, num_users=num_users))
        
    def print_users(self):
        print("== User List: ==")
        for user in self.users.values():
            print(" {name} (email: {email}, number of books: {num_books})".format
                (name=user.name, email=user.email, num_books=len(user.books)))
    
    def get_most_read_book(self):
        most = 0
        for book, num_users in self.books.items():
            if num_users > most:
                most = num_users
                most_read = book
        return most_read

    def highest_rated_book(self):
        highest = 0
        for book in self.books.keys():
            rating = book.get_average_rating()
            if rating > highest:
                highest = rating
                best_book = book
        return best_book

    def most_positive_user(self):
        highest = 0
        for user in self.users.values():
            rating = user.get_average_rating()
            if rating > highest:
                highest = rating
                positive_user = user
        return positive_user

    def get_n_most_read_books(self, n):
        most = 0
        book_list = []
        # first pass: how many times has most read book been read?
        for num_users in self.books.values():
            if num_users > most:
                most = num_users
        # now search downwards from most read book
        count = 0
        while (most > 0) and (count < n):
            print("searching for books that have been read {} times".format(most))
            for book, num_users in self.books.items():
                if num_users == most:
                    print("found book: {}".format(book.title))
                    book_list.append(book)
                    count += 1
                    if count == n:
                        break
            # next iteration: search for books with one less reader
            most -= 1
        return book_list
        
    def get_n_most_prolific_readers(self, n):
        most = 0
        reader_list = []
        # first pass: how many books has most prolific reader read?
        for user in self.users.values():
            if len(user.books) > most:
                most = len(user.books)
        # now search downwards 
        count = 0
        while (most > 0) and (count < n):
            print("searching for {} book readers".format(most))
            for user in self.users.values():
                if len(user.books) == most:
                    print("found user: {}".format(user.name))
                    reader_list.append(user)
                    count += 1
                    if count == n:
                        break
            # next iteration: search for books with one less reader
            most -= 1
        return reader_list
        



