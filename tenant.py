from flask import Blueprint, current_app, request, session, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from model import User, Tenant, Biller, BillRecord, Entity
from crud import delete_tenant, update_tenant, delete_all
from datetime import datetime

tenant = Blueprint('tenant', __name__)

@tenant.route('/tenant', methods=['GET','POST','DELETE'])
def tenants():
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        engine = current_app.engine

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
            due_date = datetime.strptime(request.form['payment_date'], "%Y-%m-%d")
            rent_rate = request.form['rent_rate']
            contact = request.form['contact']
            address = request.form['address']
            unique_id = db.query(Entity).order_by(Entity.id.desc()).first().id
            print('Assigning form data completed')
            try:
                check_if_already_registered = db.query(Tenant).filter(Tenant.name == name, Tenant.lastname == lastname).count()
                if check_if_already_registered > 0:
                    db.close()
                    return jsonify(error = str('Tenant Already Registered'))
            except Exception as e:
                db.close()
                return jsonify(error = str(e))
            
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
            return jsonify(str(f'Successfully Registered {name}'f' {lastname}'))
        except Exception as e:
            print(str(e))
            return jsonify(error=str(e))
        finally:
            db.close()


        
    if request.method == 'GET':

        try:
            tenants = db.query(Tenant).all()
            jsonarray = [tenant.to_json() for tenant in tenants]
            print("Getting Tenant List")
            db.close()
            if jsonarray:
                return jsonarray
            return 'Empty'
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred during the database query: {e}")
            # Handle the error or return an appropriate error response
        return 'Error: Failed to retrieve tenant data'



        tenants = db.query(Tenant).all()
        jsonarray = [tenant.to_json() for tenant in tenants]
        print("Getting Tenant List")
        #db.close()
        if jsonarray:
            return jsonarray
        return 'Empty'
    
    if request.method == 'DELETE':
        result = delete_all(db,Tenant)
        db.close()
        if result == 0:
            return 'Successfully Deleted'
        return 'Deletion Failed'
    
    return 'Invalid Request'
    
@tenant.route('/tenant/<int:tenant_id>', methods=['GET','PUT', 'DELETE'])
def tenant_crud(tenant_id):
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        engine = current_app.engine
    Session = sessionmaker(bind=engine)
    db = Session()
    
    if request.method == 'GET':
        if tenant_id == 0:
            pass
            #redirect('/0',)
        tenants = db.query(Tenant).filter_by(id = tenant_id).first()
        if tenants:
            return tenants.to_json()
        return 'Tenant not found!'

    if request.method == 'DELETE':
        result = delete_tenant(db,tenant_id)
        if result == 0:
            return 'Successful Deletion'
        #Request to read data where tenant id is given the result is Base Model Tenant object
        return 'Delete operation Failed'
       
    if request.method == 'PUT':
        update_data = request.get_json()
        if update_data:
            result = update_tenant(db,tenant_id,update_data)
            if result:
                print(result.name," ",result.lastname," Record Successfully Updated")
                return jsonify(str(f'Successfully Updated Record of {result.name} {result.lastname}'))
        return jsonify(error =  str('Invalid format or data submitted for update is empty! Use json format. Thank you' ))
        #Request to update data where tenant id is given the result is Base Model Tenant object
     
    return jsonify(error = str('Invalid Request'))