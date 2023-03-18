from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

from flasgger import Swagger, swag_from
from config.swagger import template, swagger_config

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
import datetime as JWT_TIME

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

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# Install OpenSSH and get a new ssh key with ssh-keygen -t rsa

private_key = open('./id_rsa', 'r').read()
print(private_key)
prKey = serialization.load_ssh_private_key(private_key.encode(), password=b'teste')

public_key = open('./id_rsa.pub', 'r').read()
pubKey = serialization.load_ssh_public_key(public_key.encode())

app.config["JWT_PRIVATE_KEY"] = prKey
app.config["JWT_PUBLIC_KEY"] = pubKey
app.config['JWT_ALGORITHM'] = 'RS256'

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_TIME.timedelta(minutes=30)
app.config['SWAGGER'] = {
    'title': 'BAP API',
    'uiversion': 3
}
key = "b96e9a4a-fd76-4a03-8080-ea53e264001a"

jwt = JWTManager(app)

limiter = Limiter(app)
date_format = "%Y-%m-%d"

api = Api(app)
spec = APISpec(
        title='Bap',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0')

api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)

app.config.update({
    'APISPEC_SPEC': spec,
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)
Swagger(app, config=swagger_config, template=template)

message_service = MessageService()
message_service = MessageDecorator(message_service)
category_service = CategoryService()
category_service = CategoryDecorator(category_service)
api_helper = APIMain(message_service)

# BapResponseSchema = Schema.from_dict(
#     {"category": fields.Str(), "description": fields.Str(), "published_at": fields.DateTime(), "source": fields.Str(), "title": fields.Str()}
# )

# class BapRequestSchema(Schema):
#     message_id = fields.Integer(metadata={"places":0})

# class APIKEYRequestSchema(Schema):
#     api_key = fields.String(metadata={"places":0})


@app.route('/authorization', methods=['POST'])
@swag_from('./docs/authorization.yaml')
def login():
        keyx = request.json.get("api_key", None)
        if keyx != key:
            return jsonify({"msg": "ApiKey Incorreta"}), 401

        access_token = create_access_token(identity=keyx)

        return jsonify(access_token=access_token)

@app.route('/all', methods=['GET'])
@limiter.limit("5 per minute")
@jwt_required()
@swag_from('./docs/all.yaml')
def get_all():
    messages = message_service.get_all_messages()
    return jsonify(messages)

@app.route('/by_id', methods=['POST'])
@jwt_required()
def get_by_id():
    return api_helper.get_by_id(request=request)

@app.route('/by_category', methods=['POST'])
@jwt_required()
def get_by_category():
    return api_helper.get_by_category(request=request)


@app.route('/between_date', methods=['POST'])
@jwt_required()
def get_between_date():
    return api_helper.get_between_date(request=request)

@app.route('/category_between_date', methods=['POST'])
@jwt_required()
def get_category_between_date():
    return api_helper.get_category_between_date(request=request)

@app.route('/messages', methods=['POST'])
@jwt_required()
def add_message():
    return api_helper.add_message(request=request)

@app.route('/messages/<int:message_id>', methods=['PUT'])
@jwt_required()
def update_message(message_id):
    return api_helper.update_message(request=request,message_id=message_id)
        
@app.route('/messages/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    response = message_service.delete_message(message_id)
    return f"Message {request.json['source']} deleted"

@app.route('/add_category', methods=['POST'])
@jwt_required()
def add_category():
    category_name = escape(request.json['category'])
    return create_category(category_name=category_name)

def create_category(category_name):
    response = category_service.create_category(categorie_name=category_name)
    return f"Message {category_name} created"

@app.route('/get_all_categories', methods=['POST'])
@jwt_required()
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
    app.run(debug=False, use_reloader=False, port=3500)

    # Terminate the scheduler process when the Flask app is stopped
    scheduler.terminate()
    
