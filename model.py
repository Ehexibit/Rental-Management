from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from app import db;



Base = declarative_base
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
        self.password = password


class Tenant(Base):

    __tablename__ = 'tenant'

    id = Column(Integer,primary_key=True)
    unique_id = Column(Integer, ForeignKey('entity.id'))
    name = Column(String, nullable=False)
    lastname = Column(String)
    email = Column(String)
    duedate = Column(Date,nullable=False)
    paiddate = Column(Date)

    entity = relationship('Entity')

    def __init__(self, unique_id, duedate, name, lastname=None, email=None, paiddate=None):
        self.unique_id = unique_id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.duedate = duedate
        self.paiddate = paiddate

class BillRecord(Base):
    __tablename__ = 'billRecord'
    id = Column(Integer,primary_key=True)
    unique_id = Column(Integer, ForeignKey('entity.id'))
    duedate = Column(Date, nullable=False)
    billstatus = Column(Enum('Paid, Unpaid'), nullable=False, default='Unpaid')
    paiddate = Column(Date)

    entity = relationship('Entity')


    def __init__(self, unique_id, duedate, paiddate=None):
        self.unique_id = unique_id
        self.duedate = duedate
        self.paiddate = paiddate

class Biller(Base):
    __tablename__ = 'biller'
    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    unique_id = Column(Integer, ForeignKey('entity.id'))

    entity = relationship('Entity')

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer,primary_key=True)


# Create the tables based on the models you can make logic
Base.metadata.create_all(db)

# Create a session
Session = sessionmaker(bind=db)
session = Session()

# Perform database operations with your models

# Close the session
session.close()