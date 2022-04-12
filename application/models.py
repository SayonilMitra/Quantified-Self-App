from flask_sqlalchemy import SQLAlchemy
import os.path

db = SQLAlchemy()

# Users

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_login_time = db.Column(db.String(100),nullable=False)
    trackers = db.relationship('Tracker', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

# Trackers 

class Tracker(db.Model):
    tracker_id = db.Column(db.Integer, primary_key=True)
    tracker_name = db.Column(db.String(80), nullable=False)
    tracker_description = db.Column(db.String(120), nullable=False)
    tracker_type = db.Column(db.String(50),nullable=False)
    user_defined_options = db.Column(db.String(200))
    tracker_log_time = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    tracker_logs = db.relationship('Trackerlogs', backref='tracker', lazy=True)


    def __repr__(self):
        return '<Tracker %r>' % self.tracker_id

# User logs of trackers

class Trackerlogs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    log_value = db.Column(db.String(100), nullable=False)
    log_note = db.Column(db.String(100))
    log_time = db.Column(db.String(80), unique=True, nullable=False)
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.tracker_id'),nullable=False)

    def __repr__(self):
        return '<Log %r>' % self.log_id

