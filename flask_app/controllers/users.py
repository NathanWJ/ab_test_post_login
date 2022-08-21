from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.experiment import Experiment
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



###################################### 
# LOGIN AND REGISTRATION 
###################################### 
@app.route('/start')
def index():
    return render_template('start.html')


@app.route('/regcheck', methods=['POST'])
def registration_check():
    if not User.validate_register(request.form):
        return redirect('/start')
    data = {
        'username': request.form['username'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/home')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_one_by_username(request.form)
    if not user:
        flash('Invalid username or password', 'login')
        return redirect('/start')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid username or password', 'login')
        return redirect('/start')
    session['user_id'] = user.id
    return redirect('/home')


###################################### 
# LOGOUT
###################################### 

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


