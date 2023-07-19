from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class database(Base):
    __tablename__ = 'Users'
    id = Column("id",Integer,primary_key=True)
    mobile_number = Column("mobile_number", String(11), unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    name = Column("name", String, nullable=False)

    def __init__(self,name,mobile_number,password):
        self.name = name
        self.mobile_number = mobile_number
        self.password = password

    def __repr__(self):
        return f"({self.name}) ({self.password}) ({self.mobile_number})"

engine = create_engine("sqlite:///mydb.db", echo=True, future=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
sessions = Session()

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    mobile_number = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(100),nullable=False)