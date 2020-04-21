import os
from models import *
from create import *
from datetime import datetime
from flask import Flask, session, render_template, request, redirect
from flask_session import Session

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/register")
def index():
    # return "Project 1: TODO"
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def show():
    if request.form["action"] == "register":
        username = request.form.get("username")

        #to check for the username availability
        all_users = User.query.all()
        all_usernames = []
        for each in all_users:
            all_usernames.append(each.username)

        if username in all_usernames:
            return render_template("register.html", flag=True)
        
        password = request.form.get("pwd")
        email = request.form.get("email")
        gender = request.form.get("gender")
        DOB = request.form.get("DOB")
        if DOB == '':
            DOB = None
        u = User(username=username, password=password, email=email, gender=gender, DOB=DOB)
        db.session.add(u)
        db.session.commit()
        return render_template("success.html")

@app.route("/admin")
def show_users():
    users = User.query.order_by(User.time_stamp.desc()).all()
    return render_template("users_table.html", users=users)

@app.route("/auth", methods=["POST"])
def authentication():
    username = request.form.get("username")
    password = request.form.get("pwd")
    user = User.query.get(username)
    if user:
        if password == user.password:
            session["username"] = username
            return redirect("/home")
        else:
            return render_template("register.html", var="mismatch")
    else:
        return render_template("register.html", var="invalid")

@app.route("/home")
def home():
    if "username" in session:
        return render_template("home.html")
    else:
        return redirect("/register")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/register")