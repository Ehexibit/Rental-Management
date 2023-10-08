
from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template, jsonify

from flask_mysqldb import MySQL



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

@get_data.route('/users', methods=['PUT'])
def user_crud():
    
    from sqlalchemy.orm import sessionmaker
    from crud import get_user_by_id

    if request.method == 'PUT':
        
        form_data = request.form
        print("Form Data Content",form_data.get('username'),form_data.get('old_password'),form_data.get('password'))
        if 'username' in form_data:
            pass
        username = form_data.get('username')
        id = session['user_id']
        old_password = form_data.get('old_password')
        password = form_data.get('password')

        with current_app.app_context():
            engine = current_app.engine
        #Create a session
        Session = sessionmaker(bind=engine)
        db = Session()
        user = get_user_by_id(db,id)
        if username is not None:
            user.username = username
        
        if old_password is not None:
            
            if user.check_password(old_password):
                if password is not None:
                    user.set_password(password)
                    db.commit()
                    db.close()
                    return jsonify(str('Successful updating password'))
                return 'Password cannot be empty' 
            
            print("Invalid password or user not found")
            return jsonify(str('Invalid Password'))
                
        return jsonify(str('Failed Updating'))
    
    return jsonify(str('POST or GET, DELETE METHOD'))

    