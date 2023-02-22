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

@app.route('/from_date', methods=['POST'])
def get_from_date():
    date_string =escape(request.json['from_date'])
    date_object = datetime.strptime(date_string, date_format)
    message = message_service.get_all_messages_from_date(from_date=date_object)
    return jsonify(message)


@app.route('/between_date', methods=['POST'])
def get_between_date():
    from_date =escape(request.json['from_date'])
    until_date =escape(request.json['until_date'])
    date_object_from = datetime.strptime(from_date, date_format)
    date_object_until = datetime.strptime(until_date, date_format)
    message = message_service.get_all_messages_between_dates(from_date=date_object_from,to_date=date_object_until)
    return jsonify(message)

@app.route('/category_between_date', methods=['POST'])
def get_category_between_date():
    category = escape(request.json['category'])
    from_date =escape(request.json['from_date'])
    until_date =escape(request.json['until_date'])
    date_object_from = datetime.strptime(from_date, date_format)
    date_object_until = datetime.strptime(until_date, date_format)
    message = message_service.get_messages_between_dates_with_category(category=category,from_date=date_object_from,to_date=date_object_until)
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
    # Schedule the task to run every day at 13:00
    #schedule.every().day.at(webscrapper_time).do(scrapperJob)
    ##schedule.every(5).minutes.do(scrapperJob)
    #schedule.every(12).hours.do(scrapperJob)

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
    