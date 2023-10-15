from flask import Flask, request, session, redirect, url_for, render_template, jsonify, current_app
from flask_mysqldb import MySQL
import os #OS command
import re #Regix pattern
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base


mysql = MySQL()
db = SQLAlchemy()

def create_app():

    app = Flask(__name__, static_url_path='/static')

    # MySQL configurations (replace with your own database information)
    password = os.environ.get('MYSQLPW')
    sqlAlchemyUri = "mysql://admin:"+password+"@localhost:3306/reman"
    app.config['MYSQL_HOST'] = 'localhost'  # Database host (e.g., localhost)
    app.config['MYSQL_USER'] = 'admin'   # Database username
    app.config['MYSQL_PASSWORD'] = password   # Database password
    app.config['MYSQL_DB'] = 'reman'   # Database name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reman/reman.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = 'sqlite:///reman/reman.db'
    app.secret_key = "TestingApplication"
    
    print("App Config - Session Duration:",app.permanent_session_lifetime)
    
    
    mysql.init_app(app)
    db.init_app(app)

    # Define the absolute path to the database file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #db_path = os.path.join(current_dir, '/reman/reman.db')
    db_path = current_dir+'/reman/reman.db'
    db_url = f'sqlite:///{db_path}'
    print("Path",db_path)
    # Create an engine that connects to the database
    engine = create_engine(db_url, echo=True)

    #engine = create_engine('mysql://', creator=lambda: mysql.connection, pool_pre_ping=True)
    #engine = create_engine('sqlite:///C:/Users/Efren/Rental-Management/reman/reman.db', echo=True)
    #engine = create_engine(db_url, echo=True)
    with app.app_context():
        app.db = db
        app.mysql = mysql
        app.engine = engine
         
        from model import init_model
        print("Init model")
        init_model()
            
    from login import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from get_data import get_data
    app.register_blueprint(get_data)
    from tenant import tenant
    app.register_blueprint(tenant,url_prefix='/tenant')
    from user import user
    app.register_blueprint(user,url_prefix='/user')

    return app

app = create_app()

@app.route('/')
def admin():

    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))
    return render_template('admin.html')

@app.route('/registration')
def registration():
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))
    return render_template('registration.html')

@app.route('/billrecords')
def billrecords():
    if not 'logged_in' in session: 
       return redirect(url_for('auth.authm'))
    return render_template('billrecord.html')

@app.route('/viewtenants')
def viewtenants():
    if not 'logged_in' in session: 
       return redirect(url_for('auth.authm'))
    return render_template('viewtenants.html')


#@app.teardown_appcontext
#def close_connection(exception):
#  db = getattr(g, '_database', None)
#   if db is not None:
#       db.close()


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
            
        
        
#def get_db():
 #   db = getattr(g, '_database', None)
  #  if db is None:
   #     db = g._database = sqlite3.connect(app.config['DATABASE'])
    
    #    db.row_factory = sqlite3.Row
    #return db
        
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
   