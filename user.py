from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template, jsonify
from model import User
from sqlalchemy.orm.exc import NoResultFound

user = Blueprint('user', __name__)


@user.route('/', methods=['GET','PUT'])
def update_user():
    if not 'logged_in' in session:
        return redirect(url_for('auth.authm'))
    
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

       
        try:
            user = db.query(User).filter_by(id = id).one()
        except NoResultFound as e:
            return jsonify(error = str(e))
        except Exception as e:
            return jsonify(error = str(e))
        
        if username is not None and username != '':
            try:
                result = db.query(User).filter(User.id != id)
                if result:
                    for res in result:
                        if res.username == username:
                            return jsonify(error = str('Username already taken!'))
                    print('Username is unique will now proceed to update')
            except Exception as e:
                return jsonify(error = str(e))
            
            user.username = username

        print(username)

        if old_password is not None:
            
            if user.check_password(old_password):
                if password is not None:
                    user.set_password(password)
                    db.commit()
                    db.close()
                    return jsonify(str('Successfully updated password'))
                db.rollback()
                return jsonify(error = str('Password cannot be empty'))
            
            print("Invalid password or user not found")
            db.rollback()
            return jsonify(error = str('Invalid Password'))
        db.rollback()        
        return jsonify(error = str('Failed Updating: Old Password not validated'))
    
  
    if request.method == 'GET':
        tenants = db.query(User).all()
        jsonarray = [tenant.to_json() for tenant in tenants]
        if jsonarray:
            return jsonarray
        return 'Empty'
    
    return jsonify(str('POST or GET, DELETE METHOD'))