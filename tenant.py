from flask import Blueprint, current_app, request, session, redirect, url_for
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Tenant, Biller, BillRecord, Entity


tenant = Blueprint('tenant', __name__)

@tenant.route('/', methods=['GET'])
def tenants():

    with current_app.app_context():
        mysql = current_app.mysql

    engine = create_engine('mysql://', creator=lambda: mysql.connection)   
    Session = sessionmaker(bind=engine)
    db = Session()

    if request.method == 'GET':
        users = db.query(User).all()
        jsonarray = [user.to_json() for user in users]
        return jsonarray
    
@tenant.route('/<int:tenant_id>', methods=['GET','POST', 'PUT', 'DELETE'])
def tenant_crud(tenant_id):
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        mysql = current_app.mysql

    engine = create_engine('mysql://', creator=lambda: mysql.connection)   
    Session = sessionmaker(bind=engine)
    db = Session()
    
    if request.method == 'POST': #INSERT DATA TO table tenant
        
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        duedate = request.form['duedate']
        rentrate = request.form['rentrate']
        contact = request.form['contact']
        unique_id = db.query(Entity).count()
        db.add(Tenant(unique_id=unique_id))
        db.add(Entity())
        db.commit()
        db.close()
    
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass
    return 'Failed Updating'
