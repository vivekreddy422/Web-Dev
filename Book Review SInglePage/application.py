import os,requests,json,xmltodict
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from datetime import datetime
from user import *
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
            return render_template("registration.html", error = True, errorMessage=errorMessage)
        else:
            user = User(userName=userName,name=name,mail=mail,password=password)
            db.session.add(user)
            db.session.commit()
            successMessage = "Registration succesful. Please Login"
            return render_template(("login.html"), success = True, successMessage = successMessage)


@app.route("/admin")
def admin():
    allUsers = User.query.order_by(User.created_on.desc()).all()
    return render_template("admin.html",allUsers = allUsers)

@app.route("/login",methods = ["POST","GET"])
def login():
    if(request.method == "POST"):
        userName = request.form.get("userName")
        password = request.form.get("password")
        flag = get_user_details(userName,password)
        if(flag):
            session["user"] = userName
            return render_template("Results.html",name = userName)
        else:
            errorMessage = "Invalid credentials.try again."
            return render_template("login.html",error = True, errorMessage = errorMessage)
    else:
        if "user" in session:
            return render_template("Results.html",name = session["user"])
        return render_template("login.html")


@app.route("/home")
def home():
    if "user" in session:
        userName = session["user"]
        return render_template("HomePage.html",name = userName)
    else:
        return redirect(url_for("login"))

@app.route("/api/search",methods = ["POST"])
def apisearch():
    searchType = request.form.get("type")
    userinput = request.form.get("query")
    allBooks = searchBooks(searchType=searchType, userinput = userinput)
    allBooks = getAllUniqueBooks(allBooks)
    allBooks_json = []
    for book in allBooks:
        eachBook = {}
        eachBook["isbn"] = book.isbn
        eachBook["title"] = book.title
        eachBook["author"] = book.author
        allBooks_json.append(eachBook)
    return jsonify({"allBooks":allBooks_json})



def searchBooks(searchType,userinput):
    search = "%{}%".format(userinput)
    if searchType == "all":
        result = Book.query.filter(or_(Book.isbn.like(search), Book.title.like(search), Book.author.like(search))).all()
        allBooks = getAllUniqueBooks(result)
    elif searchType == "isbn":
        allBooks = Book.query.filter(Book.isbn.like(search)).all()
    elif searchType == "author":
        allBooks = Book.query.filter(Book.author.like(search)).all()
    else:
        allBooks = Book.query.filter(Book.title.like(search)).all()
    return allBooks

@app.route("/api/bookpage", methods=["POST"])
def bookpage_api():
    isbn = request.form.get("isbn")
    res = Book.query.filter_by(isbn = isbn).first()
    if (res):
        book = {
            "isbn" : res.isbn,
            "author" : res.author,
            "title" : res.title,
            "year" : res.year
        }
        return jsonify({"status_code" : 200, "book" : book})
    else:
        return jsonify({"status_code" : 400})

@app.route("/api/submit-review", methods = ["POST"])
def apireview():
    if "user" in session:
        userName = session["user"]
        isbn = request.form.get("isbn")
        book = Book.query.get(isbn)
        r = Review.query.filter(and_(Review.isbn == isbn, Review.userName == userName)).first()
        if r is None:
            return jsonify({"status_code":400})
        else:
            return jsonify({"status_code":200, "rating":r.rating, "review":r.review})
    else:
        return redirect(url_for("login"))

@app.route("/submit-review", methods=["POST"])
def submit():
    if "user" in session:
        userName = session["user"]
        isbn = request.form.get("isbn")
        r = Review.query.filter(and_(Review.isbn == isbn, Review.userName == userName)).first()
        rating = request.form.get("rating")
        if rating == "null":
            rating = None
        review = request.form.get("review")
        if r is None:
            r = Review(isbn=isbn, userName=userName, rating=rating, review=review)
            db.session.add(r)
            db.session.commit()
        else:
            r.rating = rating
            r.review = review
            db.session.commit()
        return jsonify({"status_code":200, "rating":r.rating, "review":r.review})
    else:
        return redirect(url_for("login"))


# @app.route("/search",methods = ["GET","POST"])
# def search():
#     if request.method == "POST":
#         searchType = request.form.get("type")
#         userinput = request.form.get("BookDetails")
#         search = "%{}%".format(userinput)
#         if searchType == "all":
#             result = Book.query.filter(or_(Book.isbn.like(search), Book.title.like(search), Book.author.like(search))).all()
#             allBooks = getAllUniqueBooks(result)
#         elif searchType == "isbn":
#             allBooks = Book.query.filter(Book.isbn.like(search)).all()
#         elif searchType == "author":
#             allBooks = Book.query.filter(Book.author.like(search)).all()
#         else:
#             allBooks = Book.query.filter(Book.title.like(search)).all()
#         if(len(allBooks) == 0):
#             displayResult = "No results Found"
#             display_scrollBar = False
#         else:
#             display_scrollBar = True
#             displayResult = f"There are {len(allBooks)} results for the corresponding query."
#         return render_template("Results.html",Books = allBooks, displayResult = displayResult, display_scrollBar = display_scrollBar, query = userinput)
#     if request.method == "GET":
#         return redirect(url_for("home")) 
# 
def getAllUniqueBooks(result):
    if(result == None):
        return None
    else:
        temp = []
        for bookOne in result:
            flag = True
            for bookTwo in temp:
                if(bookOne.isbn == bookTwo.isbn):
                    flag = False
                    break
            if(flag):
                temp.append(bookOne)
        return temp
# 
# @app.route("/bookPage/<string:isbn>")
# def bookPage(isbn):
#     book = Book.query.filter_by(isbn = isbn).first()
#     username = session["user"]
#     # review = Review.query.filter_by(userName = username).first()
#     review = Review.query.filter(and_(Review.isbn == book.isbn, Review.userName == username)).first()
#     if review is not None:
#         review_given = True
#     else:
#         review_given = False
#     print(book.isbn)
#     return render_template("bookpage.html", review_given = review_given, book = book, review = review)



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

# @app.route("/submit-review/<string:isbn>", methods=["POST"])
# def submit(isbn):
#     if "user" in session:
#         userName = session["user"]
#     else:
#         return redirect(url_for("login"))
#     r = Review.query.filter(and_(Review.isbn == isbn, Review.userName == userName)).first()
#     rating = request.form.get("rating")
#     review = request.form.get("review")
#     print(rating)
#     if r is None:
#         r = Review(isbn=isbn, userName=userName, rating=rating, review=review)
#         db.session.add(r)
#         db.session.commit()
#     else:
#         r.rating = rating
#         r.review = review
#         db.session.commit()
#     return redirect(url_for("bookPage", isbn=isbn))


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))