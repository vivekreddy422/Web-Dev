import os
from models import *
from create import *
from datetime import datetime
from flask import Flask, session, render_template, request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jhidcdnultjgxn:d826d980191f190b67002fabead45c4966294a74e382693d59edb44441f70727@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d5flmt5uf6icgd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/register")
def index():
    # return "Project 1: TODO"
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def show():
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
    time_stamp = datetime.now()
    u = User(username=username, password=password, email=email, gender=gender, DOB=DOB, time_stamp=time_stamp)
    db.session.add(u)
    db.session.commit()
    return render_template("success.html")

@app.route("/admin")
def show_users():
    users = User.query.order_by(User.time_stamp).all()
    print(users[0].DOB)
    return render_template("users_table.html", users=users)