from sqlalchemy.orm import Session
from model import Tenant, User, Biller, BillRecord  # Replace 'your_module' with the actual module where Tenant is defined
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound

class ModelOperator:
    def __init__(self, session: Session):
        self.Session = session

    def connect_to_database(self):
        # Initialize the database connection here if needed
        pass

    def create(self, data):
        # Implement the create logic here
        pass

    def read(self, id):
        # Implement the read logic here
        session = self.Session()
        
        pass

    def update(self, id, data):
        # Implement the update logic here
        session = self.Session()
        try:
            # Retrieve the record to update
            record = session.query(self.__class__).filter_by(id=id).one()
            
            # Update the record's attributes with the data provided
            for key, value in data.items():
                setattr(record, key, value)
            
            session.commit()
            
            return record
        except NoResultFound:
            return None  # Record not found
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
        

    def delete(self, id):
        # Implement the delete logic here
        pass


#CRUD OPERATION FOR USER
def create_user(session: Session, username, email, password):
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()

def get_all_users(session: Session):
    return session.query(User).all()

def get_user_by_id(session: Session,user_id):
    return session.query(User).filter_by(id=user_id).first()

def update_user(session: Session,user_id, new_username):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.username = new_username
        session.commit()
def get_user_by_username(session: Session, username):
    return session.query(User).filter_by(username=username).first()
  
def delete_user(session: Session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()

#CRUD OPERATION FOR TENANT START HERE
def create_tenant(db: Session, unique_id: int, name: str, lastname: str, email: str, duedate: str, paiddate: str):
    new_tenant = Tenant(
        unique_id=unique_id,
        name=name,
        lastname=lastname,
        email=email,
        duedate=duedate,
        paiddate=paiddate
    )
    db.add(new_tenant)
    db.commit()

def get_tenant_by_id(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

def get_tenant_by_unique_id(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.unique_id == tenant_id).first()

def update_tenant(db: Session, tenant_id: int, name: str, lastname: str, email: str, duedate: str, paiddate: str):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        tenant.name = name
        tenant.lastname = lastname
        tenant.email = email
        tenant.duedate = duedate
        tenant.paiddate = paiddate
        db.commit()

def delete_tenant(db: Session, tenant_id: int):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        db.delete(tenant)
        db.commit()




#CRUD OPERATION FOR BILLER START HERE