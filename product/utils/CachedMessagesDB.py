from sqlalchemy import create_engine, Column, String, Integer, Identity, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

# Cachedm are approved messages
# @property nrid parameter is the id of the message
# @property summary is the main text of the message
# @property date is when the message was capture
class Cachedm(Base):
    __tablename__ = "nonr_register"
    cmid = Column("id",Integer,Identity(start=1001,cycle=True),primary_key=True)
    date_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    body = Column("body",String)
    title = Column("title",String)
    source = Column("source",String)
    categorie = Column("categorie",String)

    def __init__(self, body, title, source, categorie):
        self.body = body
        self.title = title
        self.source = source
        self.categorie = categorie

    def __repr__(self):
        return f"({self.cmid}) {self.categorie}, {self.source} - {self.summary}"

class CachedMessagesDB:
    def append(self,value):
        reference = self.session.query(Cachedm.source).filter(Cachedm.source==value.source)
        exists = self.session.query(reference.exists()).scalar()
        if exists == False:
            self.session.add(value)
            self.session.commit()
    
    def appendList(self,values):
        for value in values:
            reference = self.session.query(Cachedm.source).filter(Cachedm.source==value.source)
            exists = self.session.query(reference.exists()).scalar()
            if exists == False:
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
        return self.session.query(Cachedm).all()

    def __init__(self):
        engine = create_engine("sqlite:///cached_msgs.db",echo=True)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()