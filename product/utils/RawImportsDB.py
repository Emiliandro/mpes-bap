from sqlalchemy import create_engine, Column, String, Integer, DateTime, Identity
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

# Raw are summaries imported without modification
# @property rid parameter is the id of the message
# @property summary is the main text of the message
# @property source is the url of the message
# @property categorie is the tag of the message
# @property date is when the message was capture
class Raw(Base):
    __tablename__ = "raw_imports"
    rid = Column("rid",Integer,Identity(start=1001,cycle=True),primary_key=True)
    summary = Column("summary",String)
    source = Column("source",String)
    categorie = Column("categorie",String)
    date_created = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, summary, source, categorie):
        self.categorie = categorie
        self.source = source
        self.summary = summary

    def __repr__(self):
        return f"({self.rid}) {self.categorie}, {self.source} - {self.summary}"

class RawImportsDB:
    def append(self,value):
        self.session.add(value)
        self.session.commit()
    
    def appendList(self,values):
        for value in values:
            reference = self.session.query(Raw.source).filter(Raw.source==value.source)
            exists = self.session.query(reference.exists()).scalar()
            if exists == False:
               self.session.add(value)
            else:
                print("tried to add something that is already in the database")
        self.session.commit()

    def remove(self,value):
        self.session.delete(value)
        self.session.commit
    
    def removeList(self,values):
        for value in values:
            self.session.delete(value)
        self.session.commit() 

    def getAll(self):
        return self.session.query(Raw).all()

    def __init__(self):
        engine = create_engine("sqlite:///raw_imports.db",echo=True)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def demo(self):
        news0 = Raw("Viagem para Boa Vista","www.google.com","turismo")
        news1 = Raw("Viagem para Salvador","www.google.com","turismo")

        self.append(news0)
        self.append(news1)

        results = self.session.query(Raw).all()
        print(results)