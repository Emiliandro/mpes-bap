from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime

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

# escape function causes param to be rendered as text, preventing the execution of 
# injection script in the user’s browser or the in the api request.
from markupsafe import escape

# Flask-Limiter or Flask-RateLimiter. These libraries provide 
# easy-to-use decorators that can be used to limit the number 
# of requests made to certain endpoints in your application.
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from MessageDecorator import MessageDecorator
from MessageService import MessageService

app = Flask(__name__)
limiter = Limiter(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bulletin.db'
#db = SQLAlchemy(app)

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
    title = escape(request.json['title'])
    description = escape(request.json['description'])
    source = escape(request.json['source'])
    category = escape(request.json['category'])
    published_at = escape(request.json['published_at'])
    message = message_service.create_message(title, description, source, category, published_at)
    return jsonify(message)

@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    title = escape(request.json['title'])
    description = escape(request.json['description'])
    source = escape(request.json['source'])
    published_at = escape(request.json['published_at'])
    category = escape(request.json['category'])
    message = message_service.update_message(message_id, title, description, source,category,published_at)
    return f"Message {request.json['source']} updated"

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    response = message_service.delete_message(message_id)
    return f"Message {request.json['source']} deleted"

# ---------------------
if __name__ == '__main__':
    app.run(debug=True)
