from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from flask_mysqldb import MySQL
import os #OS command
import re #Regix pattern
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


db = SQLAlchemy()
mysql = MySQL()

def create_app():

    app = Flask(__name__, static_url_path='/static')

    # MySQL configurations (replace with your own database information)
    password = os.environ.get('MYSQLPW')
    sqlAlchemyUri = "mysql://admin:"+password+"@localhost/database_name"
    app.config['MYSQL_HOST'] = 'localhost'  # Database host (e.g., localhost)
    app.config['MYSQL_USER'] = 'admin'   # Database username
    app.config['MYSQL_PASSWORD'] = password   # Database password
    app.config['MYSQL_DB'] = 'tenant'   # Database name
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlAlchemyUri
    app.secret_key = "TestingApplication"
    
    print("App Config - Session Duration:",app.permanent_session_lifetime)
    mysql.init_app(app)
    db.init_app(app)
        
    from login import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from get_data import get_data
    app.register_blueprint(get_data)
    return app

app = create_app()

@app.route('/')
def admin():

    if not 'logged_in' in session:
        
       return redirect(url_for('auth.authm'))
    
    return render_template('admin.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/billrecords')
def billrecords():
    return render_template('billrecord.html')

@app.route('/viewtenants')
def viewtenants():
    return render_template('viewtenants.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        
        cursor = mysql.connection.cursor()
        
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['boardinghouse']
        paymentDate = request.form['paymentDate']
        rentRate = request.form['rentRate']
        #Please Add logic here to sanitize variables for query
    
        check_existing_record = "SELECT * FROM users WHERE name = '"+name+"' AND lastname = '"+lastname+"'"
        cursor.execute(check_existing_record)
        
        if cursor.fetchone():
            print("User Already Registered")
            return jsonify({'error_message': 'Tenant with this name already exists.'})
        else:
            print("Registering new user")
        
            insert_query = "INSERT INTO users (name, lastname, email, contactNumber, address, paymentDueDate, rentRate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
            cursor.execute(insert_query, (name, lastname, email, contact, address, paymentDate, rentRate))
            mysql.connection.commit()
               
            cursor.close() 
            
                  
            # You can store this data in a database or in memory, depending on your needs
            # For this example, we'll store it in memory
            print('Submitted value: ',name,email)
            #return render_template('submitted.html', name=name, email=email)
        
            if is_valid_email(email): 
                print("Successful Submission")
                return jsonify(name=name, email=email)
            else: 
                return jsonify({'error_message': 'Tenant with this name already exists.'})
            
        
        
        
#Email Validation
def is_valid_email(email):
    # Define a regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Use re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False       
    

#This Code is for testing only start here CORS
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/get_datas', methods=['GET'])
def get_data():
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

#Model User
class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

#CORS End
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)