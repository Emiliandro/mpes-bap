from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, load_only
from sqlalchemy import Column, String, Integer, DateTime, Identity
from datetime import datetime
from flask import jsonify

Base = declarative_base()

class NewsBulletin(Base):
    __tablename__ = "news_bulletin"
    id = Column("id",Integer,Identity(start=1001,cycle=True),primary_key=True)
    title = Column("title",String(100), nullable=False)
    message = Column("message",String(100), nullable=False)
    categorie = Column("categorie",String(100), nullable=False)
    source = Column("source",String(100), unique=True, nullable=False)
    date_created = Column("datetime",DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, categorie, title, message, source, date_created):
        self.title = title
        self.message = message
        self.source = source
        self.date_created = date_created
        self.categorie = categorie

    def __repr__(self):
        return f'<newsbreak {self.title}: {self.message} ({self.source})>'


class BulletinDB:
    def __init__(self):
        engine = create_engine("sqlite:///bulletin.db",echo=False)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def createAndAppend(self,formatted_request):
        news = NewsBulletin(message=formatted_request['message'], source=formatted_request['source'], title=formatted_request['title'], categorie=formatted_request['categorie'],date_created=formatted_request['date_created'])
        
        self.append(value=news)
        return jsonify(news.__repr__()), 201


    def append(self,value):
        self.session.add(value)
        self.session.commit()
    
    def appendList(self,values):
        for value in values:
            reference = self.session.query(NewsBulletin.source).filter(NewsBulletin.source==value.source)
            exists = self.session.query(reference.exists()).scalar()
            if exists == False:
               self.session.add(value)
        self.session.commit()

    def remove(self,value):
        reference = self.session.query(NewsBulletin.source).filter(NewsBulletin.source==value)
        self.session.delete(reference)
        self.session.commit
    
    def removeList(self,values):
        for value in values:
            reference = self.session.query(NewsBulletin.source).filter(NewsBulletin.source==value)
            self.session.delete(reference)
        self.session.commit() 

    def getAll(self):
        bulletin = self.session.query(NewsBulletin).all()
        return jsonify([news.__repr__() for news in bulletin])
    
    def getCategorie(self, categorie):
        return self.session.query(NewsBulletin).filter(NewsBulletin.categorie==categorie).all()
    
    def getCategories(self, categories):
        return self.session.query(NewsBulletin).options(load_only=categories).all()