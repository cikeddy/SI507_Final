from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
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

def get_or_create_utility(utility_name, mech_name):
    mechanic = get_or_create_mech(mech_name)
    utility = Utility.query.filter_by(name=utility_name).first()
    if not utility:
       utility = Utility(name=utility_name)
    utility.mechanics.append(mechanic)
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
