from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

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

api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Bap',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui',
})
docs = FlaskApiSpec(app)

message_service = MessageService()
message_service = MessageDecorator(message_service)
category_service = CategoryService()
category_service = CategoryDecorator(category_service)
api_helper = APIMain(message_service)

BapResponseSchema = Schema.from_dict(
    {"category": fields.Str(), "description": fields.Str(), "published_at": fields.DateTime(), "source": fields.Str(), "title": fields.Str()}
)


class BapRequestSchema(Schema):
    message_id = fields.Integer(metadata={"places":0})

@api.resource('/get_all')
class GetAll(MethodResource, Resource):
    @doc(description='Get All', tags=['GetAll'])
    @marshal_with(BapResponseSchema())  # marshalling
    
    def get(self):
        messages = message_service.get_all_messages()
        return jsonify(messages)

@api.resource('/by_id')
class ById(MethodResource, Resource):
    @doc(description='Post By Id.', tags=['ById'])
    @use_kwargs(BapRequestSchema, location=('json'))
    @marshal_with(BapRequestSchema)
    def post(self, **kwargs):
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
    schedule.every(1).minutes.do(scrapperJob)
    schedule.every(12).hours.do(scrapperJob)

    # Keep the scheduled tasks running in the background
    while True:
        schedule.run_pending()
        time.sleep(15)


docs.register(GetAll)
docs.register(ById)
# ---------------------
if __name__ == '__main__':
    # Start the scheduler in a separate process
    scheduler = Process(target=start_scheduler)
    scheduler.start()

    # Start the Flask web server
    app.run(debug=False, use_reloader=False)

    # Terminate the scheduler process when the Flask app is stopped
    scheduler.terminate()
    