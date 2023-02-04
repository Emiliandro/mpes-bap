from sqlalchemy import create_engine, Column, String, Integer, Identity, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

# Nonr are the historic of requests
# @property nrid parameter is the id of the message
# @property summary is the main text of the message
# @property date is when the message was capture
class Nonr(Base):
    __tablename__ = "nonr_register"
    nrid = Column("id",Integer,Identity(start=1001,cycle=True),primary_key=True)
    summary = Column("summary",String)
    date_created = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, summary):
        self.summary = summary

    def __repr__(self):
        return f"({self.nrid}) {self.summary}"

class NonRepudiationDB:
    def append(self,value):
        self.session.add(value)
        self.session.commit()
    
    def appendList(self,values):
        for value in values:
            self.session.add(value)
        self.session.commit()

    def remove(self,value):
        self.session.delete(value)
        self.session.commit
    
    def removeList(self,values):
        for value in values:
            self.session.delete(value)
        self.session.commit() 

    def getAll(self):
        return self.session.query(Nonr).all()

    def __init__(self):
        engine = create_engine("sqlite:///nonr_register.db",echo=True)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()