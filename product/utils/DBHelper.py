from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Identity
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Raw are summaries imported without modification
# @property rId parameter is the id of the message
# @property Summary is the main text of the message
# @property Source is the url of the message
# @property Categorie is the tag of the message
class Raw(Base):
    __tablename__ = "raw_imports"
    rid = Column("rid",Integer,Identity(start=1001,cycle=True),primary_key=True)
    summary = Column("summary",String)
    source = Column("source",String)
    categorie = Column("categorie",String)

    def __init__(self, summary, source, categorie):
        self.categorie = categorie
        self.source = source
        self.summary = summary

    def __repr__(self):
        return f"({self.rid}) {self.categorie}, {self.source} - {self.summary}"

class DBHelper:
    def __init__(self):
        engine = create_engine("sqlite:///raw_imports.db",echo=True)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        news0 = Raw("Viagem para Boa Vista","www.google.com","turismo")
        news1 = Raw("Viagem para Salvador","www.google.com","turismo")

        session.add(news1)
        session.add(news0)
        session.commit()

        results = session.query(Raw).all()
        print(results)