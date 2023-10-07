
from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from login import User


get_data = Blueprint('get_data', __name__)

mysql = MySQL()

@get_data.route('/get_all_data',  methods=['GET'])
def get_all_data():
    try:
        
        # Connect to the MySQL database
        cursor = mysql.connection.cursor()
              
        # Execute SQL query to fetch data
        query = "SELECT name, lastname, contactNumber, email, paymentDueDate FROM users"
        cursor.execute(query)
        
        # Fetch all the rows as a list of dictionaries
        data = cursor.fetchall()
        
        # Close the cursor and database connection
        cursor.close()
       
        
        # Convert the data to JSON and return it
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e))

@get_data.route('/get_all_tenant',  methods=['GET','POST'])
def getAllTenant():
    if 'logged_in' in session:
        
        filter = request.args.get('filter')
        if filter is not None:
            print(filter)
            return f'Your request filter is  = {filter}'
        return 'All tenant list'
        #Give all the list

    return redirect(url_for('auth.authm'))

@get_data.route('/user', methods=['GET','POST'])
def user_crud():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from model import User
    from crud import get_user_by_id

    if request.method == 'GET':
        text = request.args.get('text')
        id = request.args.get('id')

        with current_app.app_context():
            mysql = current_app.mysql
            engine = create_engine('mysql://', creator=lambda: mysql.connection)
        #Create a session
        Session = sessionmaker(bind=engine)
        db = Session()
        user = get_user_by_id(db,id)
        user.set_password(text)
        db.commit()
        db.close()
        return 'Successful updating password'
    
    return 'POST method'

    