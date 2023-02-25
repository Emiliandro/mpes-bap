from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

# escape function causes param to be rendered as text, preventing the execution of 
# injection script in the user’s browser or the in the api request.
from markupsafe import escape
from datetime import datetime 

# Flask-Limiter or Flask-RateLimiter. These libraries provide 
# easy-to-use decorators that can be used to limit the number 
# of requests made to certain endpoints in your application.
from flask_limiter import Limiter
from multiprocessing import Process

from message_decorator import MessageDecorator
from message_service import MessageService
from category_decorator import CategoryDecorator
from category_service import CategoryService
from bap_main import BapMain

# schedule module in Python to schedule a script to run once a day at a specific time. 
import schedule
import time
app = Flask(__name__)
limiter = Limiter(app)
date_format = "%Y-%m-%d"

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
category_service = CategoryService()
category_service = CategoryDecorator(category_service)

def filter_request(request):
    from_date = escape(request.json['from_date'])
    until_date = escape(request.json['until_date'])
    return {
        'category': escape(request.json['category']),
        'from_date':datetime.strptime(from_date, date_format),
        'until_date':datetime.strptime(until_date, date_format) }

@app.route('/get_all', methods=['GET'])
@limiter.limit("5 per minute")
def get_all():
    messages = message_service.get_all_messages()
    return jsonify(messages)

@app.route('/by_id', methods=['POST'])
def get_by_id():
    message_id = escape(request.json['message_id'])
    message = message_service.get_message_by_id(message_id=message_id)
    return jsonify(message)

@app.route('/by_category', methods=['POST'])
def get_by_category():
    category = escape(request.json['category'])
    message = message_service.get_message_by_category(category=category)
    return jsonify(message)

@app.route('/between_date', methods=['POST'])
def get_between_date():
    validated = filter_request(request=request)
    message = message_service.get_all_messages_between_dates(from_date=validated['from_date'],to_date=validated['until_date'])
    return jsonify(message)

@app.route('/category_between_date', methods=['POST'])
def get_category_between_date():
    validated = filter_request(request=request)
    message = message_service.get_messages_between_dates_with_category(category=validated['category'],from_date=validated['from_date'],to_date=validated['until_date'])
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

@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = escape(request.json['category'])
    return create_category(category_name=category_name)

def create_category(category_name):
    response = category_service.create_category(categorie_name=category_name)
    return f"Message {request.json['category_name']} created"

@app.route('/get_all_categories', methods=['POST'])
def get_all_categories():
    return get_categories()

def get_categories():
    messages = category_service.get_all_categorys()
    return jsonify(messages)


# ---------------------
webscrapper = BapMain()
webscrapper_time = "13:00"

def scrapperJob():
    with app.app_context():
        print("Script is running at ",webscrapper_time)
        messages = webscrapper.getMessages()
        print("in total were fetched:",len(messages),"messages in this time.")
        time.sleep(5)
        upload = message_service.create_messages(messages)
        print(upload)

def start_scheduler():
    #Schedule the task to run every day at 13:00
    #schedule.every().day.at(webscrapper_time).do(scrapperJob)
    ##schedule.every(5).minutes.do(scrapperJob)
    schedule.every(12).hours.do(scrapperJob)

    # Keep the scheduled tasks running in the background
    while True:
        schedule.run_pending()
        time.sleep(15)

# ---------------------
if __name__ == '__main__':
    # Start the scheduler in a separate process
    scheduler = Process(target=start_scheduler)
    scheduler.start()

    # Start the Flask web server
    app.run(debug=False, use_reloader=False)

    # Terminate the scheduler process when the Flask app is stopped
    scheduler.terminate()
    