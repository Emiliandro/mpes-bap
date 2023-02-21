from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

# escape function causes param to be rendered as text, preventing the execution of 
# injection script in the user’s browser or the in the api request.
from markupsafe import escape

# Flask-Limiter or Flask-RateLimiter. These libraries provide 
# easy-to-use decorators that can be used to limit the number 
# of requests made to certain endpoints in your application.
from flask_limiter import Limiter #from flask_limiter.util import get_remote_address
from MessageDecorator import MessageDecorator
from MessageService import MessageService
from bap_main import BapMain

# schedule module in Python to schedule a script to run once a day at a specific time. 
import schedule
import time

app = Flask(__name__)
limiter = Limiter(app)

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
webscrapper = BapMain()

def scrapperJob():
    print("Script is running at 13:00")
    print(webscrapper.getMessages())

schedule.every().day.at("13:00").do(scrapperJob)


# ---------------------
if __name__ == '__main__':
    app.run(debug=True)
    