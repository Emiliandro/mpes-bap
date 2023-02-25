from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, load_only
import copy


Base = declarative_base()
class Category(Base):
    __tablename__ = "saved_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def clone(self):
        return copy.deepcopy(self)

class CategoryService:
    def __init__(self):
        self.prototype = Category() 
        engine = create_engine("sqlite:///saved_categories.db",echo=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        def delete_category(self,category_id):
            pass
        
        def update_category(self,category_id, categorie_name):
            pass

        def create_categorys(self,categories):
            pass

        def create_category(self,categorie_name):
            pass

        def get_all_categorys(self):
            pass