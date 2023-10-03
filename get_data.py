
from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from login import User

get_data = Blueprint('get_data', __name__)

mysql = MySQL()
db = SQLAlchemy()


@get_data.route('/get_data',  methods=['GET'])
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