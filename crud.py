from sqlalchemy.orm import Session
from model import Tenant, User, Biller, BillRecord  # Replace 'your_module' with the actual module where Tenant is defined
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound, StaleDataError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

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

def update_tenant(db: Session, id, data):
        # Implement the update logic here
        session = db
        try:
            # Retrieve the record to update
            record = session.query(Tenant).filter_by(id=id).one()
            
            # Update the record's attributes with the data provided
            for key, value in data.items():
                setattr(record, key, value)
                print("Key:",key," Value:",value)
            session.commit()
            return record
        except NoResultFound:
            print("No Results Found")
            return None  # Record not found
        except StaleDataError:
            session.refresh(record)
            print("Object has been modified need to refresh")
            return None
        except Exception as e:
            print("An Exception Occurred check below")
            session.rollback()
            raise e
        finally:
            #session.close()
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
    return db.query(Tenant).filter(id = tenant_id).first()

def get_tenant_by_unique_id(db: Session, tenant_id: int):
    return db.query(Tenant).filter(unique_id = tenant_id).first()

def update_tenants_old_version(db: Session, tenant_id: int, name: str, lastname: str, email: str, duedate: str, paiddate: str):
    tenant = db.query(Tenant).filter(id = tenant_id).first()
    if tenant:
        tenant.name = name
        tenant.lastname = lastname
        tenant.email = email
        tenant.duedate = duedate
        tenant.paiddate = paiddate
        db.commit()

def delete_tenant(db: Session, tenant_id: int):
    try:
        tenant = db.query(Tenant)
     
        tenant.delete()
        db.commit()
        
        return 0

    except IntegrityError as e:
        print(f"Deleting Tenant Operation IntegrityError: {e}")
        db.rollback()
        return 1
    except NoResultFound as e:
        db.rollback() 
        print(f"Deleting Tenant Operation NoResultFound: {e}")
        return 2
    except Exception as e:
        print(f'Delete Tenant Operation Uncaught Exception: {e}')
        return 3
    finally:
        db.close()


#DELETE OPERATIONS FOR MODELS
def delete_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(id = user_id).one()
     
        db.delete(user)
        db.commit()
        
        return 0

    except IntegrityError as e:
        print(f"Deleting User Operation IntegrityError: {e}")
        db.rollback()
        return 1
    except NoResultFound as e:
        db.rollback() 
        print(f"Deleting User Operation NoResultFound: {e}")
        return 2
    except Exception as e:
        print('Delete User Operation Uncaught Exception')
        return 3
    finally:
        db.close()
    
def delete_biller(db: Session, biller_id: int):
    try:
        biller = db.query(Biller).filter(id = biller_id).one()
     
        db.delete(biller)
        db.commit()
        
        return 0

    except IntegrityError as e:
        print(f"Deleting Biller Operation IntegrityError: {e}")
        db.rollback()
        return 1
    except NoResultFound as e:
        db.rollback() 
        print(f"Deleting Biller Operation NoResultFound: {e}")
        return 2
    except Exception as e:
        print(f'Delete Biller Operation Uncaught Exception: {e}')
        return 3
    finally:
        db.close()

def delete_all(db: Session, Base: declarative_base):
    try:
        
        db.delete(Base)
        db.commit()
        
        return 0

    except IntegrityError as e:
        print(f"Delete All Operation IntegrityError: {e}")
        db.rollback()
        return 1
    except NoResultFound as e:
        db.rollback() 
        print(f"Deleting All Operation NoResultFound: {e}")
        return 2
    except Exception as e:
        print(f'Delete All Operation Uncaught Exception: {e}')
        return 3
    finally:
        db.close()
    
#INSERT OPERTION FOR MODELS
def insert_model(db: Session, Base: declarative_base):
    try:
        db.add(Base)
        db.commit()
        return 0
    except IntegrityError as e:
        db.rollback()
        print(f"Inserting Model Operation IntegrityError: {e}")
        return 1
    except Exception as e:
        db.rollback()
        print(f"Inserting Model Operation Error: {e}")
        return 2
    finally:
        db.close()



    

#CRUD OPERATION FOR BILLER START HERE