from bs4 import BeautifulSoup 
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import requests
import random
import csv
import os
from flask import Flask, request, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy
from SI507project_models import *
from SI507project_data import get_data, obj



app = Flask(__name__)
app.debug = False
app.use_reloader = True
app.config['SECRET_KEY'] = 'Xslfdksfojsdf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./exercises.db' 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db.init_app(app)


    

###this function will return a random exercise
def get_random_exercise():
    exercises = Exercise.query.all()
    random.shuffle(exercises)
    return exercises[1].name


######### Routes #########################
@app.route('/home')
def index():
    exercises = Exercise.query.all()
    num_exercises = len(exercises)
    return render_template('index.html',num_exercises=num_exercises)

### routes to search for an exercise 

@app.route('/search')
def form1():
    return render_template('search_form.html')

@app.route('/muscle-search')
def form2():
    return render_template('muscle_search.html')


@app.route('/result',methods=["GET"])
def result_form1():
    if request.method == "GET":
        print(request.args)
        if len(request.args) > 0:
            for k in request.args:
                exercise_name = request.args.get(k,"None").lower()
                try:
                    exercise = Exercise.query.filter_by(name=exercise_name.lower()).first()
                    utility = Utility.query.filter_by(id=exercise.utility_id).first()
                    mechanics = Mechanic.query.filter_by(id=exercise.mechanic_id).first()
                    force = Force.query.filter_by(id=exercise.force_id).first()
                    muscle = Muscle.query.filter_by(id=exercise.target_muscle_id).first()
                    return render_template('search_result.html',exercise=exercise, utility=utility, mechanics=mechanics, force=force, muscle=muscle)
                except AttributeError:
                    return render_template('invalid_search.html', item='Exercise')


### one page to request a random exercise 
@app.route('/random')
def result2_form1():
    exercise_name = get_random_exercise()
    exercise = Exercise.query.filter_by(name=exercise_name).first()
    utility = Utility.query.filter_by(id=exercise.utility_id).first()
    mechanics = Mechanic.query.filter_by(id=exercise.mechanic_id).first()
    force = Force.query.filter_by(id=exercise.force_id).first()
    muscle = Muscle.query.filter_by(id=exercise.target_muscle_id).first()
    return render_template('search_result.html',exercise=exercise, utility=utility, mechanics=mechanics, force=force, muscle=muscle)
        
### one page to request an exercise by muscle
@app.route('/muscle')
def result_form2():
    if request.method == "GET":
        if len(request.args) > 0:
                for k in request.args:
                    muscle_name = request.args.get(k, "None").lower()
                    try:
                        muscle = Muscle.query.filter_by(name=muscle_name).first()
                        exercises = Exercise.query.filter_by(target_muscle_id=muscle.id)
                        return render_template('muscle_search_result.html', muscle=muscle.name, exercises=exercises)
                    except:
                        return render_template('invalid_search.html', item='Muscle')


## one page to view all muscles
@app.route('/all-muscles')
def data_view1():
    muscles = Muscle.query.all()
    return render_template('all_muscles.html', muscles=muscles)

@app.route('/all-exercises')
def data_view2():
    exercises = Exercise.query.all()
    return render_template('all_exercises.html', exercises=exercises)



if __name__ == '__main__':
    db.create_all()
    if not Exercise.query.first():
        exercises_list= get_data(obj)
        for ex in exercises_list:
            utility = get_or_create_utility(ex.utility,ex.mechanics)
            force = get_or_create_force(ex.force)
            mechanics = get_or_create_mech(ex.mechanics)
            muscle = get_or_create_muscle(ex.target_muscle)
            get_or_create_exercise(ex.name,utility.id, force.id, mechanics.id,ex.instructions, muscle.id)
    
    app.run()