from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from application.models import User, Tracker, Trackerlogs, db
from flask import current_app as app

# create log

@app.route("/createlog/<tracker_id>",methods=["POST","GET"])
def createlog(tracker_id):
    tracker_type = Tracker.query.filter_by(tracker_id=tracker_id).first().tracker_type
    if tracker_type == "time_tracker":
        log_value_hours = request.form.get("log_value_hours")
        log_value_minutes = request.form.get("log_value_minutes")
        log_value = log_value_hours + " hours " + log_value_minutes + " minutes "
    elif tracker_type == "mo_tracker":
        options_list = Tracker.query.filter_by(tracker_id=tracker_id).first().user_defined_options.rsplit(",")
        multiple_option_input = ""
        for option in options_list:
            if request.form.get(f"log_value_{option}") is not None:
                multiple_option_input += request.form.get(f"log_value_{option}") + ","
        
        log_value = multiple_option_input.rstrip(",")
    else:
        log_value = request.form.get("log_value")
    log_note = request.form.get("log_note")
    log_time = datetime.datetime.now().strftime("%c")
    log_data = Trackerlogs(log_value=log_value,log_note=log_note,log_time=log_time,tracker_id=tracker_id)
    db.session.add(log_data)
    db.session.commit()
    return redirect(f"/trackerdetails/{tracker_id}")

# edit log details

@app.route("/editlogdetails",methods=["POST"])
def editlogdetails():
    log_id = request.form.get("log_id")
    log_value_new = request.form.get("log_value")
    log_note_new = request.form.get("log_note")
    tracker_id = request.form.get("tracker_id")

    log_data= Trackerlogs.query.filter_by(log_id=log_id).first()
    user_logs = Trackerlogs.query.filter_by(tracker_id=tracker_id).all()
    tracker = Tracker.query.filter_by(tracker_id=tracker_id).first()
    user_id = tracker.user_id
    user_name = User.query.filter_by(user_id=user_id).first().user_name

    if (log_data is None):
        error_message = "Wrong Id number, please provide correct id"
        return render_template("trackerdetails.html",user_logs=user_logs,tracker=tracker,user_name=user_name,error_message=error_message)

    if log_value_new == "":
        error_message = "Can not leave value field empty"
        return render_template("trackerdetails.html",user_logs=user_logs,tracker=tracker,user_name=user_name,error_message=error_message)

    if (log_data != None):
        if (log_data.tracker_id != tracker.tracker_id):
            error_message = "Wrong Id number, please enter correct id"       
            return render_template("trackerdetails.html",user_logs=user_logs,tracker=tracker,user_name=user_name,error_message=error_message)

    log_data.log_value = log_value_new
    if log_note_new != "":
        log_data.log_note = log_note_new
    db.session.commit()
    return redirect(f"/trackerdetails/{tracker_id}")

# delete log 

@app.route("/deletelog/<log_id>")
def deletelog(log_id):
    log_data = Trackerlogs.query.filter_by(log_id=log_id).first()
    tracker_id = log_data.tracker_id
    db.session.delete(log_data)
    db.session.commit()
    return redirect(f"/trackerdetails/{tracker_id}")
