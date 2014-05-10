from flask import Flask, make_response, request, render_template, current_app, redirect, url_for
from functools import update_wrapper
from flask_sqlalchemy import SQLAlchemy
import json
import os
import csv
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

## DATA MODELS ## 

class ClassListing(db.Model):
    __tablename__ = 'classes'
    name = db.Column(db.String(255), primary_key=True)
    def __init__(self,name):
        self.name = name

class Adjective(db.Model):
    __tablename__ = 'adjectives'
    name = db.Column(db.String(255), primary_key=True)
    def __init__(self,name):
        self.name = name

class TimePeriod(db.Model):
    __tablename__ = 'times'
    name = db.Column(db.String(255), primary_key=True)
    def __init__(self, time):
        self.name = time

class Region(db.Model):
    __tablename__ = 'regions'
    name = db.Column(db.String(50), primary_key=True)
    def __init__(self, region):
        self.name = region

class DescriptionBuzzword(db.Model):
    __tablename__ = 'descbuzz'
    name = db.Column(db.String(50), primary_key=True)
    def __init__(self,buzzword):
        self.name = buzzword

class DescriptionReality(db.Model):
    __tablename__ = 'descreality'
    name = db.Column(db.String(50), primary_key=True)
    def __init__(self,reality):
        self.name = reality

class ProfessorAdjective(db.Model):
    __tablename__ = 'professors_adj'
    name = db.Column(db.String(100), primary_key=True)
    def __init__(self,adj):
        self.name = adj

class ProfessorActivity(db.Model):
    __tablename__ = 'professors_act'
    name =db.Column(db.String(100), primary_key=True)
    def __init__(self,activity):
        self.name = activity

class AudienceSterotype(db.Model):
    __tablename__ = 'audiences_stero'
    name = db.Column(db.String(100), primary_key=True)
    def __init__(self,sterotype):
        self.name = sterotype

class AudienceDescription(db.Model):
    __tablename__ = 'audience_desc'
    name = db.Column(db.String(255), primary_key=True)
    def __init__(self,description):
        self.name = description


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
        pk = db.session.query(db.distinct(model.name)).all()[index][0]
        return model.query.get(pk)
    else:
        return None

def random_cat():
    catagory = {}
    catagory['adj'] = fetch_random(Adjective)
    catagory['time'] = fetch_random(TimePeriod)
    catagory['region'] = fetch_random(Region)
    catagory['buzzword'] = fetch_random(DescriptionBuzzword)
    catagory['reality'] = fetch_random(DescriptionReality)
    return catagory

def random_professor():
    professor = {}
    professor['adj'] = fetch_random(ProfessorAdjective)
    professor['act'] = fetch_random(ProfessorAdjective)
    return professor    

def random_audience():
    aud = {}
    aud['sterotype'] = fetch_random(AudienceSterotype)
    aud['desc'] = fetch_random(AudienceDescription)
    return aud 

def random_class():
    class_list = {}
    class_list['name'] = fetch_random(ClassListing)
    return class_list

##### DATA LOADING #### 

def load_course_data():
    import codecs
    lines = [line.strip() for line in codecs.open('./data/class-names.txt','r','utf-8')]
    for line in lines: 
        class_name = ClassListing(line)
        db.session.add(class_name)
    db.session.commit()

def load_desc_data():
    import csv
    data = csv.DictReader(open('data/course_desc.csv'))
    for row in data:
        if row['Adjectives']:
            adj = Adjective(row['Adjectives'])
            db.session.add(adj)
        if row['Time Period']:
            time = TimePeriod(row['Time Period'])
            db.session.add(time)
        if row['Region']:
            region = Region(row['Region'])
            db.session.add(region)
        if row['About (Buzzword)']:
            buzzword = DescriptionBuzzword(row['About (Buzzword)'])
            db.session.add(buzzword)
        if row['About']:
            reality = DescriptionReality(row['About'])
            db.session.add(reality)
        if row['Professor Adjective']:
            prof_adj = ProfessorAdjective(row['Professor Adjective'])
            db.session.add(prof_adj)
        if row['Who']:
            prof_desc = ProfessorActivity(row['Who'])
            db.session.add(prof_desc)
        if row['For']:
            audiences_stero = AudienceSterotype(row['For'])
            db.session.add(audiences_stero)
        if row['Other']:
            audience_desc = AudienceDescription(row['Other'])
            db.session.add(audience_desc)
    db.session.commit()

### FLASK ROUTES ### 
# FINALLY # 

@app.route('/random/', methods=['GET'])
def random_set():
    data = {}
    data['cat'] = random_cat()
    resp = make_response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/load/', methods=['GET', 'POST'])
def load():
    db.create_all()
    load_course_data()
    load_desc_data()
    return make_response('Loaded the Data')

@app.route('/drop/')
def drop():
    db.drop_all()
    return make_response('data dropped')

if __name__ == "__main__":
    app.run(debug=True)
