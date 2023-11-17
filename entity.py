from flask import Blueprint, current_app, request, session, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from model import Entity
#from datetime import datetime

entity = Blueprint('entity', __name__)

@entity.route('/entity', methods=['GET'])
def entities():
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))

    with current_app.app_context():
        engine = current_app.engine

    Session = sessionmaker(bind=engine)

    db = Session()

    try:
        entities = db.query(Entity).all()
        jsonarray = [entity.to_json() for entity in entities]
        print("Getting Entity List")
        if jsonarray:
            return jsonarray
            
        return 'Empty Entity List'
        
    except Exception as e:
        db.rollback()
        print(e)
        return 'Error Occurred'
        
    finally:
        db.close() 

    