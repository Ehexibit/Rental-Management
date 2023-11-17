from flask import Blueprint, current_app, request, session, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from model import Biller, Entity
from datetime import datetime

biller = Blueprint('biller', __name__)


@biller.route('/biller/<int:id>', methods=['PUT','DELETE'])
@biller.route('/biller', methods=['POST','GET'])
def billers(id=None):

    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        engine = current_app.engine

    Session = sessionmaker(bind=engine)

    db = Session()


    if request.method == 'POST': # Create new biller object
        try:
            name = request.form['biller_name']
            amount = request.form['amount']
            due_date = datetime.strptime(request.form['due_date'], "%Y-%m-%d")
            
            db.add(Entity(name=name))
            unique_id = db.query(Entity).order_by(Entity.id.desc()).first().id
            db.add(Biller(name=name, unique_id=unique_id, amount=amount, due_date=due_date))
            
            db.commit()

            return jsonify(f"Successfully Registering Biller {name}")
        except Exception as e:
            db.rollback()
            print(e)
        finally:
            db.close()

    if request.method == 'GET': # Query all biller objects
        try:
            billers = db.query(Biller).all()
            jsonarray = [biller.to_json() for biller in billers]
            print("Getting Biller List")
            if jsonarray:
                return jsonarray
            
            return 'Empty Biller List'
        
        except Exception as e:
            db.rollback()
            print(e)
            return 'Error Occurred'
        
        finally:
            db.close() 
        