from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship , Session
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Double, create_engine, inspect
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import bcrypt


Base = declarative_base()
#This user will be the management
class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        # Hash the password and store the hash in the 'password' field
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_json(self):
        return  { 
                    "email":  self.email,
                    "username": self.username
                    
                }

    def from_json(cls, json_data):
        return cls(json_data["username"],json_data["email"])


class Tenant(Base):

    __tablename__ = 'tenant'

    id = Column(Integer,primary_key=True)
    unique_id = Column(Integer, ForeignKey('entity.id'))
    name = Column(String(50), nullable=False)
    lastname = Column(String(50))
    email = Column(String(255))
    due_date = Column(Date,nullable=False)
    paid_date = Column(Date)
    rent_rate = Column(Double, nullable=False)
    contact = Column(Integer)
    gender = Column(Enum('Male','Female','Other'),default='Other')
    address = Column(String(150))

    entity = relationship('Entity')

    def __init__(self, unique_id, due_date, rent_rate, name, lastname=None, email=None, paid_date=None, contact=None, gender=None, address=None):
        
        self.unique_id = unique_id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.due_date = due_date
        self.paid_date = paid_date
        self.rent_rate = rent_rate
        self.contact = contact
        self.gender = gender
        self.address = address

    def to_json(self):
        return  { 
                    "name":  self.name,
                    "lastname": self.lastname,
                    "email": self.email,
                    "contact": self.contact,
                    "due_date": self.due_date
                    
                }

    def from_json(cls, json_data):
        return cls(json_data["name"],json_data["lastname"],json_data["email"],json_data["contact"],json_data["due_date"])
    

class BillRecord(Base):
    __tablename__ = 'billrecord'
    id = Column(Integer,primary_key=True)
    unique_id = Column(Integer, ForeignKey('entity.id'))
    due_date = Column(Date, nullable=False)
    bill_status = Column(Enum('Paid, Unpaid'), nullable=False, default='Unpaid')
    paid_date = Column(Date)

    entity = relationship('Entity')


    def __init__(self, unique_id, duedate, paiddate=None):
        
        self.unique_id = unique_id
        self.duedate = duedate
        self.paiddate = paiddate

class Biller(Base):
    __tablename__ = 'biller'
    id = Column(Integer,primary_key=True)
    name = Column(String(50), nullable=False)
    unique_id = Column(Integer, ForeignKey('entity.id'))

    entity = relationship('Entity')

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer,primary_key=True)

def init_model():

    from flask import current_app
    #from flask_mysqldb import MySQL
    #mysql = MySQL()
    with current_app.app_context():
        
        mysql = current_app.mysql
      
    engine = create_engine('mysql://', creator=lambda: mysql.connection)
    #Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    create_tables_if_not_exist(Base,engine)
    # Close the session when done
    session.close()
    # Check if tables exist and create them if needed

def create_tables_if_not_exist(Base,engine):

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    for table_name in Base.metadata.tables.keys():
        if table_name in existing_tables:
           
            #Base.metadata.create_all(engine,tables=[BillRecord.__table__]) -> for specific table creation
            #It will not word though if table name is already at the database so you should DROP TABLE table name firt
            Base.metadata.create_all(engine)
            print(f"Table {table_name} created.")






    