from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
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

# Flask-Limiter or Flask-RateLimiter. These libraries provide 
# easy-to-use decorators that can be used to limit the number 
# of requests made to certain endpoints in your application.
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My Message API'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Initialize encryption key
# key = Fernet.generate_key()
# fernet = Fernet(key)
# Usage example 
# encrypted_password = fernet.encrypt(data['password'].encode())
# user = User(username=data['username'], password=encrypted_password.decode())
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    source = db.Column(db.String)

# following the Single Responsibility Principle (SRP) by
# encapsulating the database operations into a separate class.
class MessageService:
    def __init__(self):
        self.prototype = MessagePrototype()

    def get_all_messages(self):
        messages = Message.query.all()
        return [self._message_to_dict(message) for message in messages]

    def get_message_by_id(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        return self._message_to_dict(message)

    def create_message(self, name, description, source):
        message = self.prototype.clone()
        message.name = name
        message.description = description
        message.source = source
        db.session.add(message)
        db.session.commit()
        return self._message_to_dict(message)

    def update_message(self, message_id, name, description, source):
        message = Message.query.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        message.name = name
        message.description = description
        message.source = source
        db.session.commit()
        return self._message_to_dict(message)

    def delete_message(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            raise ValueError("Message not found")
        db.session.delete(message)
        db.session.commit()
        return {'message': 'Message deleted successfully'}

    def _message_to_dict(self, message):
        return {'id': message.id, 'name': message.name, 'description': message.description, 'source': message.source}

# The Decorator pattern is a structural design pattern that allows behavior
# to be added to an individual object, either statically or dynamically, 
# without affecting the behavior of other objects from the same class.

# The pattern involves creating a "wrapper" class, also known as a decorator, 
# that encapsulates the original class and adds new behaviors to it by defining
# new methods or modifying existing ones. This allows the decorator to modify 
# the behavior of the object at runtime, without requiring changes to the original 
# object. The decorator pattern is useful when you want to add functionality to an 
# object in a flexible and dynamic way, without modifying the underlying code. 

# It promotes open-closed principle by allowing the extension of the behavior 
# of an object without changing the original code.
class MessageDecorator:
    def __init__(self, message_service):
        self._message_service = message_service

    def get_all_messages(self):
        messages = self._message_service.get_all_messages()
        for message in messages:
            message['source'] = '${:,.2f}'.format(message['source'])
        return messages

    def get_message_by_id(self, message_id):
        message = self._message_service.get_message_by_id(message_id)
        message['source'] = '${:,.2f}'.format(message['source'])
        return message

    def create_message(self, name, description, source):
        return self._message_service.create_message(name, description, source)

    def update_message(self, message_id, name, description, source):
        return self._message_service.update_message(message_id, name, description, source)

    def delete_message(self, message_id):
        return self._message_service.delete_message(message_id)

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
class MessagePrototype:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.source = 0.0

    def clone(self):
        return copy.deepcopy(self)

message_service = MessageService()
message_service = MessageDecorator(message_service)

@app.route('/api/messages', methods=['GET'])
@limiter.limit("5 per minute")
def get_all_messages():
    messages = message_service.get_all_messages()
    return jsonify(messages)

@app.route('/messages/<int:message_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_message(message_id):
    message = message_service.get_message_by_id(message_id)
    return jsonify(message)

@app.route('/messages', methods=['POST'])
def add_message():
    name = request.json['name']
    description = request.json['description']
    source = request.json['source']
    message = message_service.create_message(name, description, source)
    return jsonify(message)

@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    name = request.json['name']
    description = request.json['description']
    source = request.json['source']
    message = message_service.update_message(message_id, name, description, source)
    return jsonify(message)

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    response = message_service.delete_message(message_id)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
