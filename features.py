import pandas as pd
from random import randint

class Feature:
    
    def __init__(self):
        self.id = randint(1000, 9999)
        self.isbn = ""
        self.author = ""
        self.title = ""
        self.volume = 0
        self.status = True
        
        try:
            data = pd.read_csv("data/books.csv")
        except FileNotFoundError:
            self.books = []
        else:
            self.books = data.to_dict(orient="records")
            
    def isbn_generator(self):
        self.isbn += str(randint(1, 9))
        for _ in range(12):
            self.isbn += str(randint(0, 9))
        
        dupe = True
        while dupe:
            for book in self.books:
                if self.isbn == book['ISBN']:
                    self.isbn_generator()
                else:
                    dupe = False
                   
        return self.reformat_isbn(self.isbn)
    
    def user_input(self, prompt):
        if prompt == "add":
            self.get_data()
        elif prompt == "update":
            to_edit = input("Enter the ISBN of the book you want to update\n (input digits only): ")
            isbn = self.reformat_isbn(to_edit)
            self.update_data(isbn)
        elif prompt == "remove":
            to_remove = input("Enter the ISBN of the book you want to remove\n (input digits only): ")
            isbn = self.reformat_isbn(to_remove)
            self.remove_data(isbn)
        elif prompt == "exit":
            warn = input("You are about to close the program. Save changes? y/n: ").lower()
            if warn == 'y':
                self.save_data()
            self.status = False
    
    def get_data(self):
        if len(self.books) > 0:
            for book in self.books:
                if self.id == book['ID']:
                    self.id = randint(1000, 9999)
                    break
                
        self.isbn = self.isbn_generator()
        print(f"ISBN: {self.isbn}")
        self.author = input("Author: ").title()
        self.title = input("Title: ").title()
        self.volume = int(input("Volume: "))   
                
        self.record_data(self.id, self.isbn, self.author, self.title, self.volume)
        
    def record_data(self, id, isbn, author, title, volume):
        new_data = {
            "ID": id,
            "ISBN": isbn,
            "Author": author,
            "Title": title,
            "Volume": volume
        }
        self.books.append(new_data)
        
    def read_data(self):
        for book in self.books:
            print(
                "ID-%i | ISBN: %s | Author: %s | Title: %s | Volume: %i" 
                % (book['ID'], book['ISBN'], book['Author'], book['Title'], book['Volume'])
            )
            
    def update_data(self, isbn):
        book_index = None
        for book in self.books:       
            if isbn == book['ISBN']:
                book_index = self.books.index(book)
                break
        
        if book_index is None:
            print("404: Book not found.")
            self.user_input("update")
        else:
            print(f" ISBN* {self.books[book_index]['ISBN']}")
            self.books[book_index]['Author'] = input("(Update) Author: ").title()
            self.books[book_index]['Title'] = input("(Update) Title: ").title()
            self.books[book_index]['Volume'] = int(input("(Update) Volume: "))
    
    def remove_data(self, isbn):
        book_index = None
        
        for book in self.books:       
            if isbn == book['ISBN']:
                book_index = self.books.index(book)
                break
        
        author = self.books[book_index]['Author']
        title = self.books[book_index]['Title']
        volume = self.books[book_index]['Volume']
        isbn = self.books[book_index]['ISBN']    
        
        if book_index is None:
            print("404: Book not found.")
            self.user_input("remove")
        else:
            warn = input(f"You are about to remove this book\n Author: {author} | Title: {title} | Volume: {volume} | ISBN: {isbn}\n y or n: ").lower()
            if warn == 'y':
                self.books.pop(book_index)

    def reformat_isbn(self, isbn):
        isbn_update = ""
        for _ in range(len(isbn)):
            if _ == 2 or _ == 3 or _ == 9 or _ == 11:
                isbn_update += f"{isbn[_]}-"
            else:
                isbn_update += isbn[_]
        return isbn_update
    
    def save_data(self):
        df = pd.DataFrame(self.books)
        df.to_csv("data/books.csv", index=False)