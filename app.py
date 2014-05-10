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

class DescriptionBuzzword(db.Model):
    __tablename__ = 'descbuzz'
    buzzword = db.Column(db.String(50), primary_key=True)

class DescriptionReality(db.Model):
    __tablename__ = 'descreality'
    reality = db.Column(db.String(50), primary_key=True)

class ProfessorAdjective(db.Model):
    __tablename__ = 'professors_adj'
    adjective = db.Column(db.String(100), primary_key=True)

class ProfessorAdjective(db.Model):
    __tablename__ = 'professors_act'
    activty = db.Column(db.String(100), primary_key=True)

class AudienceSterotype(db.Model):
    __tablename__ = 'audiences_stero'
    sterotype = db.Column(db.String(100), primary_key=True)
    
class AudienceDescription(db.Model):
    __tablename__ = 'audience_desc'
    description = db.Column(db.String(255), primary_key=True)
    


##############################################
##  Cross Domain decorator for Flask routes ##
##############################################

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

########################
##  Stupid randomizer ##
########################

def fetch_random(model):
    count = model.query.count()
    if count:
        index = random.randint(0, count - 1)
        pk = db.session.query(db.distinct(model.url)).all()[index][0]
        return model.query.get(pk)
    else:
        return None



