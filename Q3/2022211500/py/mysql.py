import json
from sqlalchemy import Column, String, Integer, create_engine, INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://root:040818@localhost:3306/user", echo=False)
session = sessionmaker(bind=engine)
Session = session()


class ModelExt(object):
    def __repr__(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return json.dumps(fields)


class User(Base, ModelExt):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Email(Base, ModelExt):
    __tablename__ = "email"

    id = Column(Integer, primary_key=True)
    email = Column(String(20))
    user = Column(String(20))
    sqm = Column(String(20))

    def __init__(self, email, user, sqm):
        self.user = user
        self.email = email
        self.sqm = sqm
