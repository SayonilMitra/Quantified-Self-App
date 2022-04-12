from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from application.models import User, Tracker, Trackerlogs, db
from flask import current_app as app


# form to create tracker

@app.route("/tracker/<user_name>")
def tracker(user_name):
    return render_template("tracker.html",user_name=user_name)

# create tracker

@app.route("/createtracker/<user_name>",methods=["GET","POST"])
def create_tracker(user_name):
    tracker_name = request.form.get("tracker_name")
    tracker_description = request.form.get("tracker_description")
    tracker_type = request.form.get("tracker_type")
    if tracker_type == "mo_tracker":
        user_defined_options = request.form.get("user_defined_options")
    else:
        user_defined_options=""
    tracker_log_time = datetime.datetime.now().strftime("%c")
    user_id = User.query.filter_by(user_name=user_name).first().user_id
    tracker_data = Tracker(tracker_name=tracker_name,tracker_description=tracker_description,tracker_type=tracker_type,tracker_log_time=tracker_log_time,user_id=user_id,user_defined_options=user_defined_options)
    db.session.add(tracker_data)
    db.session.commit()
    return redirect(f"/dashboard/{user_name}")

# Go to tracker's detailed info page

@app.route("/trackerdetails/<tracker_id>")
def trackerdetails(tracker_id):
    user_logs = Trackerlogs.query.filter_by(tracker_id=tracker_id).all()
    user_id = Tracker.query.filter_by(tracker_id=tracker_id).first().user_id
    user_name = User.query.filter_by(user_id=user_id).first().user_name
    tracker = Tracker.query.filter_by(tracker_id=tracker_id).first()
    tracker_name = tracker.tracker_name
    tracker_description = tracker.tracker_description
    tracker_log_time = tracker.tracker_log_time
    tracker_type = tracker.tracker_type
    if tracker_type == "mo_tracker":
        user_defined_options = Tracker.query.filter_by(tracker_id=tracker_id).first().user_defined_options
        options_list = user_defined_options.rsplit(",")
        return render_template("trackerdetails.html",user_logs=user_logs,tracker=tracker,user_name=user_name,options_list=options_list)
    if tracker_type == "numerical_tracker":
        labels = [user_log.log_id for user_log in user_logs]
        values = [float(user_log.log_value) for user_log in user_logs]
        return render_template("trackerdetails.html",user_logs=user_logs,tracker=tracker,user_name=user_name,labels=labels,values=values)
    return render_template("trackerdetails.html",user_logs=user_logs,tracker=tracker,user_name=user_name)
# Delete tracker

@app.route("/deletetracker/<tracker_id>",methods=["GET","POST"])
def deletetracker(tracker_id):
    # delete logs related to that tracker
    delete_logs = Trackerlogs.__table__.delete().where(Trackerlogs.tracker_id==tracker_id)
    db.session.execute(delete_logs)
    db.session.commit()
    # delete selected tracker
    tracker = Tracker.query.filter_by(tracker_id=tracker_id).first()
    db.session.delete(tracker)
    db.session.commit()
    current_user_id = tracker.user_id
    current_user_name = User.query.filter_by(user_id=current_user_id).first().user_name
    return redirect(f"/dashboard/{current_user_name}")

# form to edit tracker

@app.route("/edittrackerform/<tracker_id>")
def edittrackerform(tracker_id):
    return render_template("edittracker.html",tracker_id=tracker_id)

# edit tracker

@app.route("/edittracker/<tracker_id>",methods=["POST"])
def edittracker(tracker_id):
    edited_tracker_name = request.form.get("tracker_name")
    edited_tracker_description = request.form.get("tracker_description")
    tracker = Tracker.query.filter_by(tracker_id=tracker_id).first()
    tracker.tracker_name = edited_tracker_name
    tracker.tracker_description = edited_tracker_description
    db.session.commit()
    return redirect(f"/trackerdetails/{tracker_id}")