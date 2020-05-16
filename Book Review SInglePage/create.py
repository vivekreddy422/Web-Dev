import os

from flask import Flask, render_template, request
from models import *
import csv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    db.create_all()
    file = open("books.csv")
    allBooks = csv.reader(file)
    for book in allBooks:
        details = Book(isbn=book[0], title=book[1],author=book[2], year=int(book[3]))
        db.session.add(details)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()