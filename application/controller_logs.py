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

# form to edit log

@app.route("/editlogform/<log_id>")
def editlogform(log_id):
    tracker_id = Trackerlogs.query.filter_by(log_id=log_id).first().tracker_id
    tracker = Tracker.query.filter_by(tracker_id=tracker_id).first()
    if tracker.tracker_type == "mo_tracker":
        options_list = Tracker.query.filter_by(tracker_id=tracker_id).first().user_defined_options.rsplit(",")
        return render_template("editlog.html",log_id=log_id,tracker=tracker,options_list=options_list)
    return render_template("editlog.html",log_id=log_id,tracker=tracker)

# edit log

@app.route("/editlog/<log_id>",methods=["POST"])
def editlog(log_id):
    tracker_id = Trackerlogs.query.filter_by(log_id=log_id).first().tracker_id
    tracker_type = Tracker.query.filter_by(tracker_id=tracker_id).first().tracker_type
    if tracker_type == "time_tracker":
        log_value_hours = request.form.get("log_value_hours")
        log_value_minutes = request.form.get("log_value_minutes")
        edited_log_value = log_value_hours + " hours " + log_value_minutes + " minutes "
    elif tracker_type == "mo_tracker":
        options_list = Tracker.query.filter_by(tracker_id=tracker_id).first().user_defined_options.rsplit(",")
        multiple_option_input = ""
        for option in options_list:
            if request.form.get(f"log_value_{option}") is not None:
                multiple_option_input += request.form.get(f"log_value_{option}") + ","
        
        edited_log_value = multiple_option_input.rstrip(",")
    else:
        edited_log_value = request.form.get("log_value")
    edited_log_note = request.form.get("log_note")
    log_data = Trackerlogs.query.filter_by(log_id=log_id).first()
    tracker_id = log_data.tracker_id
    log_data.log_value = edited_log_value
    log_data.log_note = edited_log_note
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
