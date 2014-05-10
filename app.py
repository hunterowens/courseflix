from flask import Flask, make_response, request, render_template, current_app, redirect, url_for
from functools import update_wrapper
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

## DATA MODELS ## 

class ClassListing(db.Model):
    __tablename__ = 'classes'
    dept = db.Column(db.String(4), unique = False)
    number = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(255), primary_key=True)

class Adjective(db.Model):
    __tablename__ = 'adjectives'
    name = db.Column(db.String(255), primary_key=True)

class TimePeriod(db.Model):
    __tablename__ = 'times'
    time = db.Column(db.String(255), primary_key=True)

class Region(db.Model):
    __tablename__ = 'regions'
    region = db.Column(db.String(50), primary_key=True)

class Description(db.Model):
    __tablename__ = 'desc'
    id = db.Column(db.Integer, primary_key=True)
    buzzword = db.Column(db.String(50))
    reality = db.Column(db.String(50))

class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    adjective = db.Column(db.String(100))
    activty = db.Column(db.String(100))

class Audience(db.Model):
    __tablename__ = 'audiences'
    id = db.Column(db.Integer, primary_key=True)
    sterotype = db.Column(db.String(100))
    description = db.Column(db.String(255))

