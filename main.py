from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from application.models import User, Tracker, Trackerlogs, db

app= None

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

app.secret_key = 'sjgbdklkdsnvknwvenjdnjvdaejfwenw'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

from application.controller_login import *
from application.controller_logs import *
from application.controller_tracker import *
from application.dashboard import *

if not os.path.exists("database.sqlite"):
    db.create_all()


if __name__=="__main__":
    app.run(debug=True)
