from flask import Blueprint, current_app, request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Tenant, Biller, BillRecord, Entity


tenant = Blueprint('tenant', __name__)

@tenant.route('/', methods=['GET','POST'])
def tenants():
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        mysql = current_app.mysql

    engine = create_engine('mysql://', creator=lambda: mysql.connection)   
    Session = sessionmaker(bind=engine)
    db = Session()
    
    if request.method == 'POST': #INSERT DATA TO table tenant
        print("Requesting body from route /tenant")
        print(request.method," is used")
        try:
            print(request.form)
            name = request.form['name']
            lastname = request.form['lastname']
            email = request.form['email']
            due_date = request.form['payment_date']
            rent_rate = request.form['rent_rate']
            contact = request.form['contact']
            address = request.form['address']
            unique_id = db.query(Entity).count()
            print('Assigning form data completed')

            db.add(
                Tenant(
                    name = name,
                    lastname = lastname,
                    unique_id = unique_id,
                    email = email,
                    due_date = due_date,
                    rent_rate = rent_rate,
                    contact = contact,
                    address = address
                ))
            db.add(Entity())
            db.commit()
            db.close()
            return jsonify(str(f'Successfully Registered {name}'f' {lastname}'))
        except Exception as e:
            print(str(e))
            return jsonify(error=str(e))
        
    if request.method == 'GET':
        tenants = db.query(Tenant).all()
        jsonarray = [tenant.to_json() for tenant in tenants]
        return jsonarray

    
@tenant.route('/<int:tenant_id>', methods=['GET','PUT', 'DELETE'])
def tenant_crud(tenant_id):
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        mysql = current_app.mysql

    engine = create_engine('mysql://', creator=lambda: mysql.connection)   
    Session = sessionmaker(bind=engine)
    db = Session()

    if request.method == 'GET':
        #Request to read data where tenant id is given the result is Base Model Tenant object
        pass
       
    if request.method == 'PUT':
        #Request to update data where tenant id is given the result is Base Model Tenant object
        pass
    if request.method == 'DELETE':
        #Request to delete data where tenant id is given the result is Base Model Tenant object if id is 0 then delete all
        pass
    return 'Failed Updating'
