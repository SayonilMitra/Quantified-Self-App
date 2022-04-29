from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from application.models import User, Tracker, Trackerlogs, db
from flask import current_app as app

# Home page

@app.route("/")
def index():
    return render_template("login.html",title="Login")

# login page

@app.route("/login",methods=["POST","GET"])
def log_in():
    user_name = request.form.get("user_name")
    password = request.form.get("password")

    # Check if user name exists
    user_name_test = User.query.filter_by(user_name=user_name).first()

    if user_name == "":
        return render_template("login.html",login_error_msg="User name can not be empty",title="Login")
    elif password == "":
        return render_template("login.html",login_error_msg="Password can not be empty",title="Login")
    elif user_name_test == None:
        return render_template("login.html",login_error_msg="User not found, please create new account",title="Login")
    elif password != user_name_test.password:
        return render_template("login.html",login_error_msg="Wrong password, please try again",title="Login")
    else:
        session["user_name"] = user_name
        return redirect(f"/dashboard/{user_name}")

# Sign up page

@app.route("/register",methods=["POST"])
def register():
    user_name = request.form.get("user_name")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    # check if user mame exists
    is_user_name_present = User.query.filter_by(user_name=user_name).first()
    if is_user_name_present != None:
        return render_template("login.html",signup_error_msg="Username not available, try a different one",title="Login")
    if password1 != password2:
        return render_template("login.html",signup_error_msg="passwords must match",title="Login")

    last_login_time = datetime.datetime.now().strftime("%c")
    user_login_data = User(user_name=user_name,password=password1,last_login_time=last_login_time)
    db.session.add(user_login_data)
    db.session.commit()
    session["user_name"] = user_name
    return redirect(f"/dashboard/{user_name}")

# logging out user

@app.route("/logout/<user_name>")
def log_out(user_name):
    current_user = User.query.filter_by(user_name=user_name).first()
    current_user.last_login_time = datetime.datetime.now().strftime("%c")
    db.session.commit()
    session.pop('user_name', None)
    #return session
    return redirect("/")

# Guest view

@app.route("/guest/dashboard")
def guest_dashboard():
    return render_template("guest_dashboard.html")


@app.route("/guest/tracker_demo")
def guest_tracker_info():
    return render_template("guest_tracker_demo.html")