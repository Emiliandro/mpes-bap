from sqlalchemy import create_engine, Column, String, Integer, Identity, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class Researches(Base):
    __tablename__ = "researches"
    id = Column("id",Integer,Identity(start=1001,cycle=True),primary_key=True)
    when = Column(DateTime(timezone=True), default=datetime.utcnow)
    categorie = Column("categorie",String)
    token = Column("token",String)

    def __init__(self, categorie, token):
        self.categorie = categorie
        self.token = token

    def __repr__(self):
        return f"({self.id}) {self.categorie}"

class ResearchesDB:
    def append(self,value):
        request = Researches(categorie=value['categorie'],token=value['token'])
        self.session.add(request)
        self.session.commit()
    
    def appendList(self,values):
        for value in values:
            request = Researches(categorie=value['categorie'],token=value['token'])
            self.session.add(request)
        self.session.commit()

    def getAll(self):
        return self.session.query(Researches).all()

    def __init__(self):
        engine = create_engine("sqlite:///researches.db",echo=True)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()