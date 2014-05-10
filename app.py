from flask import Flask, make_response, request, render_template, current_app, redirect, url_for
from functools import update_wrapper
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

## DATA MODELS ## 

class class_listing(db.Model):
    __tablename__ = 'classes'
    dept = db.Column(db.String(4), unique = False)
    number = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(255), primary_key=True)


