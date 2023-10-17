
from flask import Blueprint, current_app, jsonify
from flask import request, session, redirect, url_for, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from model import User

auth = Blueprint('auth',__name__)

db = SQLAlchemy()

@auth.route('/')
def authm():
    with current_app.app_context():
        engine = current_app.engine

    Session = sessionmaker(bind=engine)
    db = Session()
    result = db.query(User).count()
    if result == 0:
        return 'Create Account Please'
    return render_template('login.html')
    #return f'{result}'


@auth.route('/signup', methods=['GET','POST'])
def signup():
       
        with current_app.app_context():
            engine = current_app.engine

        Session = sessionmaker(bind=engine)
        db = Session()

        if request.method == 'POST':

            if session['access'] == 'superadmin': # if 'access' in session == 'superadmin': is bug
                
                name = request.form['username']
                password = request.form['password']
                email = request.form['email']
                access = request.form['account-type']

                print(f"Signing up user: {name} email:{email} access:{access}")
                #name = request.args.get('name')
                #password = request.args.get('password')
                try:
                    print(f"Signing up user: {name} email:{email} access:{access}")
                    db.add(User(name,email,password,access))
                    db.commit()
                    return jsonify("Account Created Successfully!")
                except Exception as e:
                    db.rollback()
                    print(e)
                    return jsonify(error = str(e))
                finally:
                    db.close()
            else:
                print("Authentication Failed")
                return redirect(url_for('auth.authm'))
                

        if request.method == 'GET':
            return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        #With actual user validation logic (e.g., database query)
        #if request.form['username'] == 'admin' and request.form['password'] == 'your@pass@word':
        #   session['logged_in'] = True
        #  return redirect(url_for('admin'))
        #else:
        #    return 'Login Failed'
        #The following code will be the correct way to handle user log in
        from crud import get_user_by_username
        with current_app.app_context():
           engine = current_app.engine
        #Create a session
        Session = sessionmaker(bind=engine)
        db = Session()
        username = get_user_by_username(db, request.form['username'])

        if(username is not None):
            if(username.check_password(request.form['password'])):
                
                session['logged_in'] = True
                session['user_id'] = username.id
                session['username'] = username.username
                session['access'] = username.access
                db.close()
                if session['access'] == 'superadmin':
                    print("Access level: ",session['access'])
                    return redirect(url_for('admin',admin_name=session['username'],access_type="super"))
                else:
                    return redirect(url_for('admin',admin_name=session['username']))       
                #return redirect(url_for('admin',admin_name=username.username))
                 
            return render_template('login.html',status_response="Invalid Credentials")
        db.close()
        return render_template('login.html',status_response="User is not registered")
        
    print("Session Logged In: ",'logged_in' in session)
    if 'logged_in' in session:
        if 'access' in session == 'superadmin':
            return redirect(url_for('admin',admin_name=session['username'],access_type="admin"))
        else:
            return redirect(url_for('admin',admin_name=session['username']))
    else:
        return redirect(url_for('auth.authm'))

@auth.route('/logout',methods=['GET', 'POST'])
def logout():

    print('Log out method = ', request.method)

    if 'logged_in' in session:
        print("Session Logged In:",'logged_in' in  session)
        session.pop('logged_in')
        print("Session Logged In:",'logged_in' in  session)
        return redirect(url_for('auth.login'))    
    return redirect(url_for('auth.login'))

    #if request.method == ['POST']:
    #    print('Log out method = POST') 
    #   if 'logged_in' in session:
    #       print('logged_in' in  session)
    #       session.pop('logged_in')
    #       return redirect(url_for('auth.login'))
        
   

@auth.route('/dashboard', methods=['GET','POST'])
def dashboard():

    if not session.get('logged_in'):
        print('Sorry folks you cant log in')
        return redirect(url_for('auth.authm'))
    return redirect(url_for('admin',admin_name="None"))
    
    