from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"
    userName = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime(),default = datetime.now(), nullable=False)

class Book(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = "Reviews"
    isbn = db.Column(db.String, ForeignKey("Books.isbn"))
    userName = db.Column(db.String, ForeignKey("Users.userName"))
    rating = db.Column(db.Integer)
    review = db.Column(db.String)

    __table_args__ = (PrimaryKeyConstraint("isbn", "userName"),)