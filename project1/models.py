from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    gender = db.Column(db.String)
    DOB = db.Column(db.Date())
    time_stamp = db.Column(db.DateTime(), nullable=False)