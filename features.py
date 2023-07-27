import pandas as pd
from random import randint

class Feature:
    
    def __init__(self):
        self.id = randint(1000, 9999)
        self.author = ""
        self.title = ""
        self.volume = 0
        self.isbn = ""
        self.status = True
        
        try:
            data = pd.read_csv("data/books.csv")
        except FileNotFoundError:
            self.books = []
        else:
            self.books = data.to_dict(orient="records")      
    
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
        print(self.id)    
        self.isbn = ""
        new_isbn = ""
        self.author = input("Author: ").title()
        self.title = input("Title: ").title()
        self.volume = int(input("Volume: "))   
        
        while len(self.isbn) != 13:
            self.isbn = str(input("ISBN: "))
            if len(self.isbn) < 13 or len(self.isbn) > 13:
                print("Invalid ISBN: Must be 13-digit long.")
            else:
                new_isbn = self.reformat_isbn(self.isbn)
                
            for book in self.books:
                if new_isbn == book['ISBN']:
                    print(" This ISBN is already in use")
                    self.isbn += "1"
                    self.get_data()
                    break
                
        self.record_data(self.id, self.author, self.title, self.volume, new_isbn)
        
    def record_data(self, id, author, title, volume, isbn):
        new_data = {
            "ID": id,
            "Author": author,
            "Title": title,
            "Volume": volume,
            "ISBN": isbn
        }
        self.books.append(new_data)
        
    def read_data(self):
        for book in self.books:
            print(
                "ID-%i | Author: %s | Title: %s | Volume: %i | ISBN: %s" 
                % (book['ID'], book['Author'], book['Title'], book['Volume'], book['ISBN'])
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