from flask import Blueprint, current_app
from flask import request, session, redirect, url_for, render_template, jsonify
from model import User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError

user = Blueprint('user', __name__)


@user.route('/user', methods=['GET','PUT'])
@user.route('/user/<int:uid>', methods=['GET','PUT'])
def update_user(uid=None):
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
        except MultipleResultsFound as e:
            return jsonify(error = str(e))
        except Exception as e:
            return jsonify(error = str(e))
        
        if username is not None and username != '':
            try:
                result = db.query(User).filter(User.id != id).all()
                
                if result:
                    for res in result:
                        if res.username == username:
                            return jsonify(error = str('Username already taken!'))
                print('Username is unique will now proceed to update')
            except Exception as e:
                db.rollback()
                return jsonify(error = str(e))
                #return jsonify(error = "Exception found check log",error_code = str(e))
            finally:
                db.close()
            
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
    
    if request.method == 'POST':
         pass
         #user create from submitted form get username email and password return the usernamme as successfull
         #call it from client /user method='POST' body = formData(form)

    if request.method == 'GET':
        if session['access'] == 'superadmin' and uid is None:
            users = db.query(User).all()
            jsonarray = [user.to_json() for user in users]
            if jsonarray:
                return jsonarray
        #The following code will create a bug loop    
        #return redirect(url_for('admin',admin_name=session['username']))
        return 'User dont have access' #This line will return when a username user log in instead of admin.html
        #Which is causing a bug because will create url end point localhost/user since our root endpoint localhost/<param_username>
        #Alternative solution is create or home on end point localhost/home/<param_username> or add param on /user endpoint /user/<int:id> 
        #But since we use this endpoint without param_id '/user/<int:id>' when updating password we can't just add param_id
        #The trick is add another endpoint where it takes no paramter but the problem will still occure we cant still use
        #redirect so the last solution is add home on our root end point in that way we can safely use the /user end point or let's just
        #create a meaningful end point like this localhost/api/user by adding api we can avoid issues on root endpoint
        #How about this 
        #localhost/ root
        #localhost/auth/
        #localhost/api/  => will accept simple form and accept or return json objects /api/user api/tenant api/billrecord api/bill
    
    return jsonify(str('POST or GET, DELETE METHOD'))