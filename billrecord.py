from flask import Blueprint, current_app, request, session, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from model import BillRecord, Entity
from datetime import datetime

billrecord = Blueprint('billrecord', __name__)

@billrecord.route('/billrecord/<int:id>', methods=['GET','PUT','DELETE'])
@billrecord.route('/billrecord', methods=['POST','GET','DELETE'])
def billrecords(id=None):

    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        engine = current_app.engine

    Session = sessionmaker(bind=engine)

    db = Session()

    if request.method == 'GET':

        if id is None: #If route is GET api/billrecord no param such as api/billrecord/id where id is billrecord.id
        #Get all new billrecord entries
            try:
                billrec = db.query(BillRecord).all()
                jsonarray = [bill.to_json() for bill in billrec]
                if jsonarray:
                    return jsonarray
                return 'Empty Bill Record List'
            except Exception as e:
                print(e)
                db.rollback()
                return jsonify(f"An exception occurred {e}")
            finally:
                db.close()
        else:
            try:
                billrec = db.query(BillRecord).filter_by(id=id).first()
                
                if billrec:
                    return billrec.to_json()
                return jsonify(f'BillRecord with id = {id} is not found')
            except Exception as e:
                print(e)
                db.rollback()
                return jsonify(f"An exception occurred {e}")
            finally:
                db.close()
           
    if request.method == 'POST':
        #Create new billrecord entry

        pass
       
    if request.method == 'PUT':
        #update existing billrecord entry
        pass
    if request.method == 'DELETE':
        #delete billrecord entry/entries
        if id is None:
            try:
                db.delete(BillRecord).all()
                db.commit()
                return jsonify(f"Successfully Deleted All Table content")
            except Exception as e:
                print(e)
                db.rollback()
                return jsonify(f"An exception occurred {e}")
            finally:
                db.close()
        else:
            try:
                billrec = db.delete(BillRecord).filter_by(id = id).one()
                db.commit()
                return jsonify(f"Successfully Deleted Table content {id}")
            except Exception as e:
                print(e)
                db.rollback()
                return jsonify(f"An exception occurred {e}")
            finally:
                db.close()
