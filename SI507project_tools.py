from bs4 import BeautifulSoup 
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import requests
import random
import csv
import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy
from SI507project_data import exercises_list



app = Flask(__name__)
app.debug = False
app.use_reloader = True
app.config['SECRET_KEY'] = 'Xslfdksfojsdf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./exercises.db' 
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
    name = db.Column(db.String(64))
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


def get_or_create_exercise(exercise_name, utility, force, mechanic,instructions, target_muscle):
    exercise = Exercise.query.filter_by(name=exercise_name).first()
    if exercise:
        return exercise
    else:
        exercise = Exercise(name=exercise_name, utility_id=utility, force_id=force, mechanic_id=mechanic,instructions=instructions, target_muscle_id=target_muscle)
        session.add(exercise)
        session.commit()
        return exercise

def get_or_create_utility(utility_name):
    utility = Utility.query.filter_by(name=utility_name).first()
    if utility:
        return utility
    else:
        utility = Utility(name=utility_name)
        session.add(utility)
        session.commit()
        return utility
    
def get_or_create_mech(mech_name):
    mechanic = Mechanic.query.filter_by(name=mech_name).first()
    if mechanic:
        return mechanic
    else:
        mechanic = Mechanic(name=mech_name)
        session.add(mechanic)
        session.commit()
        return mechanic
    
def get_or_create_force(force_name):
    force = Force.query.filter_by(name=force_name).first()
    if force:
        return force
    else:
        force = Force(name=force_name)
        session.add(force)
        session.commit()
        return force

def get_or_create_muscle(muscle_name):
    muscle = Muscle.query.filter_by(name=muscle_name).first()
    if muscle:
        return muscle
    else:
        muscle = Muscle(name=muscle_name)
        session.add(muscle)
        session.commit()
        return muscle
    
    



######### testing out adding to the database#########
for ex in exercises_list:
    utility = get_or_create_utility(ex.utility)
    force = get_or_create_force(ex.force)
    mechanics = get_or_create_mech(ex.mechanics)
    muscle = get_or_create_muscle(ex.target_muscle)
    get_or_create_exercise(ex.name,utility.id, force.id, mechanics.id,ex.instructions, muscle.id)
    session.commit()

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




        