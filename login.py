
from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy


auth = Blueprint('auth',__name__)

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@auth.route('/')
def authm():
    return render_template('registration.html')


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
        # Replace with your actual user validation logic (e.g., database query)
        if request.form['username'] == 'user' and request.form['password'] == 'password':
            session['logged_in'] = True
            print(redirect(url_for(dashboard)))
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed'
    return redirect(url_for('admin'))

@auth.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not session.get('logged_in'):
        print('Sorry folks you cant log in')
        return redirect(url_for('login'))
    
    return render_template('admin.html')