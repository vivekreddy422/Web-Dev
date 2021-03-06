import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
# os.environ["DATABASE_URL"] = "postgres://jhidcdnultjgxn:d826d980191f190b67002fabead45c4966294a74e382693d59edb44441f70727@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d5flmt5uf6icgd"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jhidcdnultjgxn:d826d980191f190b67002fabead45c4966294a74e382693d59edb44441f70727@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d5flmt5uf6icgd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, pubyear in reader:
        book = Book(isbn = isbn, title = title, author = author, year = pubyear)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()