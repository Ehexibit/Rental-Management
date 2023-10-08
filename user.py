from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template, jsonify
from model import User

user = Blueprint('user', __name__)


@user.route('/', methods=['GET','PUT'])
def update_user():
    
    from sqlalchemy.orm import sessionmaker
    from crud import get_user_by_id

    with current_app.app_context():
        engine = current_app.engine
      #Create a session
    Session = sessionmaker(bind=engine)
    db = Session()

    if request.method == 'PUT':
        
        form_data = request.form
        print("Form Data Content",form_data.get('username'),form_data.get('old_password'),form_data.get('password'))
        if 'username' in form_data:
            pass
        username = form_data.get('username')
        id = session['user_id']
        old_password = form_data.get('old_password')
        password = form_data.get('password')

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
    
  
    if request.method == 'GET':
        tenants = db.query(User).all()
        jsonarray = [tenant.to_json() for tenant in tenants]
        if jsonarray:
            return jsonarray
        return 'Empty'
    
    return jsonify(str('POST or GET, DELETE METHOD'))