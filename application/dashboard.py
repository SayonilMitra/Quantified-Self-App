from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from application.models import User, Tracker, Trackerlogs, db
from flask import current_app as app

# User dashboard

@app.route("/dashboard/<user_name>")
def dashboard(user_name):
    if "user_name" in session:
        current_user = User.query.filter_by(user_name=user_name).first()
        last_login_time = current_user.last_login_time
        user_id = current_user.user_id
        user_trackers = Tracker.query.filter_by(user_id=user_id).all()
        return render_template("dashboard.html",user_name=user_name,title="Dashboard",last_login_time=last_login_time,usertrackers=user_trackers)
    else:
        return redirect("/")

