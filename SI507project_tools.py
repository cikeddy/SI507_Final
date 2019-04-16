from bs4 import BeautifulSoup 
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import requests
import csv
import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = False
app.use_reloader = True
app.config['SECRET_KEY'] = 'Xslfdksfojsdf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./exercises_muscles.db' 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app) 
session = db.session 

### Models ###

##association Table between exercise and mechanics
exercise_groups = db.Table('exercise_groups',db.Column('exercise_id',db.Integer, db.ForeignKey('exercises.id')),db.Column('utility_id',db.Integer, db.ForeignKey('utilities.id')))




class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    utility = db.relationship('Utility', secondary=exercise_groups, backref=db.backref('exercises',lazy='dynamic'),lazy="dynamic")
    mechanics = db.Column(db.String(64))
    force = db.Column(db.String(64))
    instructions = db.Column(db.String(64))
    target_muscle = db.Column(db.Integer, db.ForeignKey('muscles.id'))

    
#    def __repr__(self):
#        return "{} by {} | {}".format(self.name)
#    
class Utility(db.Model):
    __tablename__ = "utilities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    exercises = db.relationship('Exercise', secondary=exercise_groups, backref=db.backref('utilities',lazy='dynamic'),lazy="dynamic")
#
class Muscle(db.Model):
    __tablename__ = "muscles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    body_part = db.Column(db.String(64))
    exercise = db.Column(db.Integer, db.ForeignKey('exercises.id'))
#    
    
    


###########



FILENAME = "exrx_cache.json"

program_cache = Cache(FILENAME) 


#exploring one exercise page
base_url = "https://exrx.net/WeightExercises/Sternocleidomastoid/CBNeckFlx"

data = program_cache.get(base_url)
if not data:
    data = requests.get(base_url).text

    program_cache.set(base_url, data, expire_in_days=10) # this data isn't going to change very much

soup = BeautifulSoup(data, "html.parser")

obj =  soup.find_all("div", class_="col-sm-6")[1]
muscles = soup.find('a', href = "../../Kinesiology/Glossary#Target").next_sibling.next_sibling

           
#muscles = obj.find("a", href="../../Kinesiology/Glossary#Target")
#
#obj_2 = soup.find_all("div", target_="_parent").element

#obj = [tag for tag in soup.find_all('a', class_="col-sm-6") if tag.href == "https://exrx.net/Kinesiology/Glossary#Target")

#target_element = soup.find_parent('a', href= "../../Kinesiology/Glossary#Target")
#
#
#print(target_element)

#
#print(muscles)

                    
#function to pull all of the exercise links 
#function to randomize which exercise is returned 

#
#class Exercise():
#    def __init__(self, page):
#        self.name = page.find("h1").text
#        self.utility = []
#        self.mechanics = page.find_all("td")[3].text
#        self.force = page.find_all("td")[5].text
#        self.instructions = page.find_all("p")[2].text +page.find_all("p")[4].text
#        self.target_muscle = page.find_all("div", class_="col-sm-6")[1].find_all("ul")[0].text
#    
#        for child in page.find_all('td')[1].find_all('a'):
#            self.utility.append(child.text)
#        
#new_ex = Exercise(soup)
#
##print(new_ex.utility)
#
#with open("muscles.csv","r",encoding="utf8") as f:
#    reader = csv.reader(f)
#    data = []
#    for i in reader:
#        data.append(i)
#
#class Muscle():
#    def __init__(self, row):
#        self.name = row[0]
#        self.body_part = row[1]
#        
#new_mus = Muscle(data[1])

#print(new_mus.body_part)

if __name__ == '__main__':
    db.create_all() 
    app.run()




        