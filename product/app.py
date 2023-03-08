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
from api_main import APIMain

# schedule module in Python to schedule a script to run once a day at a specific time. 
import schedule
import asyncio
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
        'app_name': 'BAPs API'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
message_service = MessageService()
message_service = MessageDecorator(message_service)
category_service = CategoryService()
category_service = CategoryDecorator(category_service)
api_helper = APIMain(message_service)

@app.route('/get_all', methods=['GET'])
@limiter.limit("5 per minute")
def get_all():
    messages = message_service.get_all_messages()
    return jsonify(messages)

@app.route('/by_id', methods=['POST'])
def get_by_id():
    return api_helper.get_by_id(request=request)

@app.route('/by_category', methods=['POST'])
def get_by_category():
    return api_helper.get_by_category(request=request)

@app.route('/between_date', methods=['POST'])
def get_between_date():
    return api_helper.get_between_date(request=request)

@app.route('/category_between_date', methods=['POST'])
def get_category_between_date():
    return api_helper.get_category_between_date(request=request)

@app.route('/messages', methods=['POST'])
def add_message():
    return api_helper.add_message(request=request)

@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    return api_helper.update_message(request=request,message_id=message_id)
        
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
    return f"Message {category_name} created"

@app.route('/get_all_categories', methods=['POST'])
def get_all_categories():
    return jsonify(get_categories())

def get_categories():
    messages = category_service.get_all_categorys()
    return messages

# ---------------------
webscrapper = BapMain()

async def do_scrapp():
    with app.app_context():
        print("Script is running at ",datetime.now())

        categories_to_fetch = get_categories()
        webscrapper.set_categories(categories_to_fetch)

        messages = webscrapper.get_messages()
        print("in total were fetched:",len(messages),"messages in this time.")
            
        upload = message_service.create_messages(messages)
        print(upload)

def scrapperJob():
    asyncio.run(do_scrapp())

def start_scheduler():
    #schedule.every(1).minutes.do(scrapperJob)
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
    