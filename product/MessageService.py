from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, load_only
from MessagePrototype import MessagePrototype
from datetime import datetime

Base = declarative_base()
date_format = "%Y-%m-%d" #"%Y-%m-%d %H:%M:%S"
class Message(Base):
    __tablename__ = "made_messages"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(255))
    source = Column(String)
    category = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)


# following the Single Responsibility Principle (SRP) by
# encapsulating the database operations into a separate class.
class MessageService:
    def __init__(self):
        self.prototype = MessagePrototype() 
        engine = create_engine("sqlite:///made_messages.db",echo=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_messages(self):
        messages = Message.query.all()
        return [self._message_to_dict(message) for message in messages]

    def get_message_by_id(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        return self._message_to_dict(message)

    def get_message_between_dates(self,from_date,to_date):
        messages = Message.query.filter(Message.published_at.between(from_date, to_date)).all()
        return [self._message_to_dict(message) for message in messages]

    def create_message(self, title, description, source, category, date_string):
        message = self.prototype.clone()
        message.title = title
        message.description = description
        message.source = source
        message.category = category
        try:
            message.published_at = datetime.strptime(date_string, date_format)
        except:
            return { "error": "Invalid datetime}" }
        self.session.add(message)
        self.session.commit()
        return self._message_to_dict(message)

    def update_message(self, message_id, title, description, source):
        message = Message.query.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        message.title = title
        message.description = description
        message.source = source
        self.session.commit()
        return self._message_to_dict(message)

    def delete_message(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        self.session.delete(message)
        self.session.commit()
        return {'message': 'Message deleted successfully'}

    def _message_to_dict(self, message):
        return {
                'id': message.id, 
                'title': message.title, 
                'description': message.description, 
                'source': message.source, 
                'published_at': message.published_at, 
                'category':message.category
            }
