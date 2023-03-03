from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, load_only
from datetime import datetime
import copy

# Fernet is a symmetric encryption algorithm and one of the recommended 
# encryption methods provided by the cryptography library in Python. 
# Fernet encryption uses a 128-bit AES (Advanced Encryption Standard) key 
# and also provides key rotation and message authentication. It is a 
# high-level interface for symmetric encryption that makes it easy to 
# encrypt and decrypt data. Fernet encryption is useful in scenarios 
# where you want to store sensitive data, such as passwords or personal 
# information, in a database or send it over the internet. Fernet ensures 
# that the data is kept confidential by encrypting it, and also guarantees 
# the integrity of the data by verifying that it has not been tampered 
# with during transmission.
# from cryptography.fernet import Fernet

# Initialize encryption key
# key = Fernet.generate_key()
# fernet = Fernet(key)
# Usage example 
# encrypted_password = fernet.encrypt(data['password'].encode())
# user = User(username=data['username'], password=encrypted_password.decode())

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

    # The Prototype pattern is a creational design pattern that allows an object 
    # to create duplicate objects or clones of itself, without depending on specific classes.

    # The pattern involves creating a prototype object that serves as a template for 
    # creating other objects. When a new object is needed, a clone of the prototype is 
    # created and modified as needed. This approach allows the creation of new objects 
    # with minimal overhead, and it allows objects to be created dynamically at runtime, 
    # without requiring a specific class to be known in advance.

    # The Prototype pattern is useful in situations where creating an object is expensive 
    # or complex, and where there are many variations of a similar object. By using a prototype,
    # you can easily create new objects by cloning an existing one and modifying its properties 
    # as needed, which can save time and resources.

    # Additionally, the Prototype pattern can promote encapsulation and reduce coupling by 
    # separating the client code from the object creation process.
    def clone(self):
        return copy.deepcopy(self)

# following the Single Responsibility Principle (SRP) by
# encapsulating the database operations into a separate class.
class MessageService:
    def __init__(self):
        self.prototype = Message() 
        engine = create_engine("sqlite:///made_messages.db",echo=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_messages(self):
        messages = self.session.query(Message).all()
        return [self._message_to_dict(message) for message in messages]
    
    def get_message_by_category(self, category):
        messages = self.session.query(Message).filter(Message.category==category)
        if messages is None:
            raise ValueError("Messages not found")
        return [self._message_to_dict(message) for message in messages]

    def get_message_by_id(self, message_id):
        message = self.session.query(Message).get(message_id)
        if message is None:
            raise ValueError("Message not found")
        return self._message_to_dict(message)

    def get_message_between_dates(self,from_date,to_date):
        messages = self.session.query(Message).filter(Message.published_at.between(from_date, to_date))
        return [self._message_to_dict(message) for message in messages]
    
    def get_messages_between_dates_with_category(self,from_date,to_date,category):
        messages = self.session.query(Message).filter(Message.category==category).filter(Message.published_at.between(from_date, to_date)) 
        return [self._message_to_dict(message) for message in messages]

    def create_messages(self,messages):
        for msg in messages:
            message = self.prototype.clone()
            message.title = msg['title']
            message.description = msg['description']
            message.source = msg['source']
            message.category = msg['category']
            #try:
            #    message.published_at = datetime.strptime(msg.date_string, date_format)
            #except:
            #    return { "error": "Invalid datetime}" }
            self.session.add(message)
        self.session.commit()
        return {'response':'added'}

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
        message = self.session.query(Message).get(message_id)
        if message is None:
            raise ValueError("Message not found")

        message.title = title
        message.description = description
        message.source = source
        self.session.commit()
        return self._message_to_dict(message)

    def delete_message(self, message_id):
        message = self.session.query(Message).get(message_id)
        if message is None:
            raise ValueError("Message not found")

        self.session.delete(message)
        self.session.commit()
        return {'message': 'Message deleted successfully'}

    def _message_to_dict(self, message):
        return {
                'title': message.title, 
                'description': message.description, 
                'source': message.source, 
                'published_at': message.published_at, 
                'category':message.category
               }
