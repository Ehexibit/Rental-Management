
from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from model import User


auth = Blueprint('auth',__name__)

db = SQLAlchemy()

@auth.route('/')
def authm():
    return render_template('login.html')


@auth.route('/signup', methods=['GET','POST'])
def signup():
        db = current_app.db
        if request.method == 'POST':
            name = request.form[name]
            password = request.form[password]
            
        name = request.args.get('name')
        password = request.args.get('password')
        
        db.session.add(User(name,password))
        db.session.commit()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = current_app.db
        # Replace with your actual user validation logic (e.g., database query)
        if request.form['username'] == 'user' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            if 'logged_in' in session:
                session.pop('logged_in')
            print('logged_in' in session)
            return 'Login Failed'
    return redirect(url_for('authm'))

@auth.route('logout',methods=['POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@auth.route('/dashboard', methods=['GET','POST'])
def dashboard():

    if not session.get('logged_in'):
        print('Sorry folks you cant log in')
        return redirect(url_for('authm'))
    return redirect(url_for('admin'))
    
    