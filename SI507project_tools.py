from bs4 import BeautifulSoup 
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import requests
import random
import csv
import os
from flask import Flask, request, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy
from SI507project_models import *



app = Flask(__name__)
app.debug = False
app.use_reloader = True
app.config['SECRET_KEY'] = 'Xslfdksfojsdf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./exercises.db' 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db.init_app(app)


    
###this function will return two random exercises that are different from each other but based on a user entry of muscle
def get_random_exercises_m(muscle):
    exercises = Exercise.query.filter_by(target_muscle=muscle).all()
    data = random.shuffle(exercises)
    exercise_lst = []
    for i in data[:1]:
        exercise_lst.append(Exercise(i))
    return exercise_lst

###this function will return two random exercises that are different from each other but based on a user entry of muscle
def get_random_exercise():
    exercises = Exercise.query.all()
    random.shuffle(exercises)
    return exercises[1].name



######### testing out adding to the database#########
#for ex in exercises_list:
#    utility = get_or_create_utility(ex.utility,ex.mechanics)
#    force = get_or_create_force(ex.force)
##    mechanics = get_or_create_mech(ex.mechanics)
#    muscle = get_or_create_muscle(ex.target_muscle)
#    get_or_create_exercise(ex.name,utility.id, force.id, mechanics.id,ex.instructions, muscle.id)
#

######################################################


######### Routes #########################
@app.route('/home')
def index():
    exercises = Exercise.query.all()
    num_exercises = len(exercises)
    return "<h1> Welome to the Exercise Generator!</h1> <p>There are currently {} exercises in the database</p>".format(num_exercises)
#    return render_template('index.html', num_movies=num_movies)
    

### routes to search for an exercise 

@app.route('/search')
def form1():
    return render_template('search_form.html')


@app.route('/result',methods=["GET"])
def result_form1():
    if request.method == "GET":
        print(request.args)
        if len(request.args) > 0:
            for k in request.args:
                exercise_name = request.args.get(k,"None")
                exercise = Exercise.query.filter_by(name=exercise_name).first()
                utility = Utility.query.filter_by(id=exercise.utility_id).first()
                mechanics = Mechanic.query.filter_by(id=exercise.mechanic_id).first()
                force = Force.query.filter_by(id=exercise.force_id).first()
                muscle = Muscle.query.filter_by(id=exercise.target_muscle_id).first()
                if not exercise:
                    return "Exercise does not exist"
            return render_template('search_result.html',exercise=exercise, utility=utility, mechanics=mechanics, force=force, muscle=muscle)

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
        
### one page to request a workout by 




############# testing out the csv ######################
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
    if not db.session.query(Exercise).first():
        db.create_all()
    app.run()