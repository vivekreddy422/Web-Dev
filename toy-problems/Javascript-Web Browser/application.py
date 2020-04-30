import os
# from models import *
# from create import *
from datetime import datetime
from flask import Flask, session, render_template, request, redirect
from flask_session import Session

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)

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
        password = request.form.get("pwd")
        email = request.form.get("email")
        if username == "vivek" and password == "123Vv@":
            return render_template("success.html")
        else:
            return "400"