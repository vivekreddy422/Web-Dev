import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/register")
def index():
    # return "Project 1: TODO"
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def show():
    username = request.form.get("username")
    password = request.form.get("pwd")
    print(username + " " + password)
    s = "Username: " + username + "\n"  + "Password: "
    for each in password:
        s += "*"
    return s