from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.experiment import Experiment
from flask_app.models.user import User

###################################### 
# DEFAULT ROUTE
###################################### 

@app.route('/')
def default():
    return redirect('/start')


###################################### 
# ROUTE TO HOME
###################################### 

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "user_id":session['user_id'],#user_id as the foreign key within experiments
        "id":session['user_id'] #id for the user query
    }
    treatment_group = Experiment.treatment_assignment(user_id)
    return render_template('home.html', experiments=treatment_group, user=User.get_one_by_id(user_id))
