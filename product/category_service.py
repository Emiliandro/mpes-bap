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
        message = self.session.query(Category).get(category_id)
        if message is None:
            raise ValueError("Message not found")

        self.session.delete(message)
        self.session.commit()
        return {'message': 'Message deleted successfully'}
        
    def update_category(self,category_id, categorie_name):
        message = self.session.query(Category).get(category_id)
        if message is None:
            raise ValueError("Message not found")

        message.name = categorie_name
        self.session.commit()
        return self._message_to_dict(message)

    def create_categorys(self,categories):
        for msg in categories:
            message = self.prototype.clone()
            message.name = msg['name']
            self.session.add(message)
        self.session.commit()
        return {'response':'added'}

    def create_category(self,categorie_name):
        message = self.prototype.clone()
        message.name = categorie_name
        self.session.add(message)
        self.session.commit()
        return self._message_to_dict(message)

    def get_all_categorys(self):
        messages = self.session.query(Category).all()
        return [self._message_to_dict(message) for message in messages]

    def _message_to_dict(self, category):
        return { 'id': category.id, 'category': category.name, }