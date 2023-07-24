import pandas as pd
from features import Feature
from art import title_art
from clear import clear

feat = Feature() 

while feat.status:
    clear()
    print(title_art)
    feat.read_data()
    if len(feat.books) < 1:
        print("There are currently no books in the directory\n ADD BOOK NOW")
        feat.get_data()               
    else:
        print("Do you want to add, update or remove a book?")
        prompt = input("  Type add/update/remove accordingly: ").lower()
        feat.user_input(prompt)
