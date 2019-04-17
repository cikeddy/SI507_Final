from bs4 import BeautifulSoup 
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import requests
import random
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

##association Table between exercise and utilities
exercise_groups = db.Table('exercise_groups',db.Column('mechanic_id',db.Integer, db.ForeignKey('mechanics.id')),db.Column('utility_id',db.Integer, db.ForeignKey('utilities.id')))


#
class Utility(db.Model):
    __tablename__ = "utilities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    mechanics = db.relationship('Mechanic', secondary=exercise_groups, backref=db.backref('utilities',lazy='dynamic'),lazy="dynamic")


class Muscle(db.Model):
    __tablename__ = "muscles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    exercises = db.relationship('Exercise',backref = 'Muscle')
#
class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    exercises = db.relationship('Exercise',backref = 'Mechanic')

class Force(db.Model):
    __tablename__ = "forces"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    exercises = db.relationship('Exercise',backref = 'Force')
    
# exercise class will only include name and instructions, everything else will be foreignkeys to other attributes
class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    instructions = db.Column(db.String(64))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'))
    force_id = db.Column(db.Integer, db.ForeignKey('forces.id'))
    target_muscle_id = db.Column(db.Integer, db.ForeignKey('muscles.id'))
    utility_id = db.Column(db.Integer, db.ForeignKey('utilities.id'))





#    def __repr__(self):
#        return "{} by {} | {}".format(self.name)
    

### Helper functions ###


def get_or_create_exercise(exercise_name, description):
    exercise = Exercise.query.filter_by(name=exercise_name).first()
    if exercise:
        return exercise
    else:
        exercise = Exercise(name=exercise_name,instructions=description)
        session.add(exercise)
        session.commit()
        return exercise

def get_or_create_muscle(muscle_name):
    muscle = Muscle.query.filter_by(name=muscle_name).first()
    if muscle:
        return muscle
    else:
        muscle = Muscle(name=muscle_name)
        session.add(muscle)
        session.commit()
        return muscle
    
    


###########



FILENAME = "exrx_cache.json"

program_cache = Cache(FILENAME) 


#exploring one exercise page
base_url = "https://exrx.net/WeightExercises/Sternocleidomastoid/CBNeckFlx"

data = program_cache.get(base_url)
if not data:
    data = requests.get(base_url).text

    program_cache.set(base_url, data, expire_in_days=10) # this data isn't going to change very much


print(type(data))

soup = BeautifulSoup(data, "html.parser")

obj =  soup.find_all("div", class_="col-sm-6")[1]

print(type(soup))


#### this variable (ex_pages) will be a list of all the links to exercise pages
## will write a function that pulls links from the directory and concatinates with base url to produce full URL and returns the list ex_pages

def get_exercise_links(start_page):
    ex_pages = []
    return ex_pages


##this function will return two random exercises that are different from each other but based on a user entry of muscle
def get_random_exercises(muscle):
    exercises = Exercise.query.filter_by(target_muscle=muscle).all()
    random.shuffle(exercises)
    exercise_lst = []
    for i in data[:1]:
        exercise_lst.append(Exercise(i))
    return exercise_lst

#### trying something out to find the target muscle
#muscles = soup.find('a', href = "../../Kinesiology/Glossary#Target").next_sibling.next_sibling

           
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

                    

#function to randomize which exercise is returned 

#
class ExerciseObj():
    def __init__(self, page):
        self.name = page.find("h1").text
        self.utility = []
        self.mechanics = page.find_all("td")[3].text
        self.force = page.find_all("td")[5].text
        self.instructions = page.find_all("p")[2].text +page.find_all("p")[4].text
        self.target_muscle = page.find_all("div", class_="col-sm-6")[1].find_all("ul")[0].text
    
        for child in page.find_all('td')[1].find_all('a'):
            self.utility.append(child.text)
        
#new_ex = ExerciseObj(soup)

#print(new_ex.utility)
#


######### testing out adding to the database#########
#new_ex_utility = Utility(name=new_ex.utility[0])
#session.add(new_ex_utility)
#session.commit()
#
#
#new_ex_muscle = Muscle(name=new_ex.target_muscle)
##session.add(new_ex_utility)
#session.add(new_ex_muscle)
#session.commit()
#session.add(Exercise(name=new_ex.name,utility_id=new_ex_utility.id,mechanics=new_ex.mechanics,force=new_ex.force,instructions=new_ex.instructions, target_muscle=new_ex_muscle.id))
#session.commit()
######################################################

######### testing out the csv ######################
#with open("muscles.csv","r",encoding="utf8") as f:
#    reader = csv.reader(f)
#    data = []
#    for i in reader:
#        data.append(i)
#
#class MuscleRow():
#    def __init__(self, row):
#        self.name = row[0]
#        self.body_part = row[1]
#        
#    def __str__(self):
#        return "{} is part of the {}".format(self.name,self.body_part)
#    
#muscles = []    
#for row in data:
#    muscles.append(MuscleRow(row))
    

#for muscle in muscles:
#    new_entry = Muscle(name=muscle.name,body_part=muscle.body_part)
#    session.add(new_entry)
#    session.commit()

#print(new_mus.body_part)

#####################################################


if __name__ == '__main__':
    db.create_all() 




        