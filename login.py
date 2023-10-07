
from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from model import User

auth = Blueprint('auth',__name__)

db = SQLAlchemy()

@auth.route('/')
def authm():
    return render_template('login.html')


@auth.route('/signup', methods=['GET','POST'])
def signup():
        from model import init_model
        myModel = init_model()
        if myModel == 'Success':
            return 'Successful Creating Table'
        else: return 'Table Already Exist'

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
        #if request.form['username'] == 'admin' and request.form['password'] == 'your@pass@word':
        #   session['logged_in'] = True
        #  return redirect(url_for('admin'))
        #else:
        #    return 'Login Failed'
        #The following code will be the correct way to handle user log in
        from crud import get_user_by_username
        with current_app.app_context():
            mysql = current_app.mysql
            engine = create_engine('mysql://', creator=lambda: mysql.connection)
        #Create a session
        Session = sessionmaker(bind=engine)
        db = Session()
        username = get_user_by_username(db, request.form['username'])
        #db.close()
        if(username is not None):
            if(username.check_password(request.form['password'])):
                session['logged_in'] = True
                session['user_id'] = username.id
                return redirect(url_for('admin'))
            
            return 'Log in failure due to incorrect credentials'
        return 'Log in failure due to user not registered'
        
    print('logged_in' in session)
    if 'logged_in' in session:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('auth.authm'))

@auth.route('/logout',methods=['GET', 'POST'])
def logout():
    if request.method == ['POST']:
        print('Log out method = POST') 
        if 'logged_in' in session:
            print('logged_in' in  session)
            session.pop('logged_in')
            return redirect(url_for('auth.login'))
        
    print('Log out method = GET')
    if 'logged_in' in session:
        print('logged_in' in  session)
        session.pop('logged_in')
        return redirect(url_for('auth.login'))    
    return redirect(url_for('auth.login'))

@auth.route('/dashboard', methods=['GET','POST'])
def dashboard():

    if not session.get('logged_in'):
        print('Sorry folks you cant log in')
        return redirect(url_for('authm'))
    return redirect(url_for('admin'))
    
    