import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from datetime import datetime

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# # app.config["SESSION_PERMANENT"] = False
# # app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# # Set up database
# # engine = create_engine(os.getenv("DATABASE_URL"))
# # db = scoped_session(sessionmaker(bind=engine))
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db.init__app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.secret_key = "secret key"
# session = {}

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/register", methods = ["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("registration.html")
    elif request.method == "POST":
        userName = request.form.get("userName")
        name = request.form.get("name")
        mail = request.form.get("email")
        password = request.form.get("password")
        if(User.query.get(userName) is not None):
            errorMessage = "UserName not available"
            alert = True
            return render_template("registration.html",errorMessage=errorMessage, alert = alert)
        else:
            user = User(userName=userName,name=name,mail=mail,password=password)
            db.session.add(user)
            db.session.commit()
            return render_template("succesfulregisteration.html",name = userName)

@app.route("/admin")
def admin():
    allUsers = User.query.order_by(User.created_on.desc()).all()
    return render_template("admin.html",allUsers = allUsers)

@app.route("/login",methods = ["POST","GET"])
def login():
    if(request.method == "POST"):
        userName = request.form.get("userName")
        password = request.form.get("password")
        userObj = User.query.get(userName)
        if((userObj is not None) and (userObj.password == password)):
            session["user"] = userName
            return redirect(url_for("home"))
        else:
            errorMessage = "Invalid credentials.try again."
            alert = True
            return render_template("login.html", errorMessage = errorMessage, alert = True)

    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")
        # return render_template("LoginPage.html")


@app.route("/home")
def home():
    if "user" in session:
        userName = session["user"]
        return render_template("HomePage.html",name = userName)
    else:
        return redirect(url_for("login"))


@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "POST":
        searchType = request.form.get("type")
        userinput = request.form.get("BookDetails")
        print("searchType: ", searchType)
        if searchType == "all":
            search = "%{}%".format(userinput)
            BooksFromisbn = Book.query.filter(Book.isbn.like(search)).all()
            BooksFromtitle = Book.query.filter(Book.title.like(search)).all()
            BooksFromauthor = Book.query.filter(Book.author.like(search)).all()
            resultOne = getAllUniqueBooks(BooksFromisbn, BooksFromtitle)
            resultTwo = getAllUniqueBooks(resultOne, BooksFromauthor)
            if(resultTwo == None):
                displayResult = "No results Found."
                return render_template("Results.html",displayResult = resultTwo)
            else:
                displayResult = f"There are {len(resultTwo)} results for the corresponding query."
                return render_template("Results.html",Books = resultTwo,displayResult = displayResult)
        elif searchType == "Isbn":
            search = "%{}%".format(userinput)
            BooksFromisbn = Book.query.filter(Book.isbn.like(search)).all()
            return render_template("Results.html",Books = BooksFromisbn)
        elif searchType == "author":
            search = "%{}%".format(userinput)
            BooksFromtitle = Book.query.filter(Book.author.like(search)).all()
            return render_template("Results.html",Books = BooksFromtitle)
        elif searchType == "title":
            search = "%{}%".format(userinput)
            BooksFromauthor = Book.query.filter(Book.title.like(search)).all()
            return render_template("Results.html",Books = BooksFromauthor)
    
def getAllUniqueBooks(firstList, secondList):
    if(firstList == None and secondList == None):
        return None
    elif(firstList == None):
        return secondList
    elif(secondList == None):
        return firstList
    else:
        firstList.extend(secondList)
        temp = []
        for bookOne in firstList:
            flag = True
            for bookTwo in temp:
                if(bookOne.isbn == bookTwo.isbn):
                    flag = False
                    break
            if(flag):
                temp.append(bookOne)
        return temp


@app.route("/bookPage/<string:isbn>")
def bookPage(isbn):
    return "bookPage"

@app.route("/review/<string:isbn>")
def review(isbn):
    if "user" in session:
        userName = session["user"]
    else:
        return redirect(url_for("login"))
    book = Book.query.get(isbn)
    r = Review.query.filter(and_(Review.isbn == isbn, Review.userName == userName)).first()
    if r is None:
        return render_template("ReviewPage.html", book=book, exists=False)
    else:
        review_text = r.review
        rating = r.rating
        return render_template("ReviewPage.html", book=book, rating=rating, review_text=review_text, exists=True)

@app.route("/submit-review/<string:isbn>", methods=["POST"])
def submit(isbn):
    if "user" in session:
        userName = session["user"]
    else:
        return redirect(url_for("login"))
    r = Review.query.filter(and_(Review.isbn == isbn, Review.userName == userName)).first()
    rating = request.form.get("rating")
    review = request.form.get("review")
    print(rating)
    if r is None:
        r = Review(isbn=isbn, userName=userName, rating=rating, review=review)
        db.session.add(r)
        db.session.commit()
    else:
        r.rating = rating
        r.review = review
        db.session.commit()
    return redirect(url_for("bookPage", isbn=isbn))

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))