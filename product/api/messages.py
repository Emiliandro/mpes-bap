from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from api.model.basic_request import BasicRequest
from utils.CachedMessagesDB import CachedMessagesDB as cmDB

api = Blueprint('messages',__name__,url_prefix='/messages')

# Cached Messages DB contain all messages approved to be sent by the api
cm_helper = cmDB()

# check if values are valide for request
def basic_request_validations(basic_request):
    is_br = isinstance(basic_request,BasicRequest)
    return is_br

# check if token is valid, this is TBD
def token_validation(token):
    if isinstance(token,str) == False:
        return False
    return True

def get_all():
    return cm_helper.getAll()

def create_request_model(msg):

    user_token = escape(msg['token'])
    msg_categ = escape(msg['categorie'])
    start_date = escape(msg['start_date'])
    end_date = escape(msg['end_date'])

    return BasicRequest(token=user_token,categorie=msg_categ,start_time=start_date,end_time=end_date)
        

@api.route('/fetch', methods=['POST'])
def fetch_categories():
    if request.method == 'POST':
        msg = request.json
        basic_request = create_request_model(msg=msg)
        
        if basic_request_validations(basic_request):
            print(f"user wants {basic_request}")
            
            if basic_request.categorie == "all":
                return get_all()
    
    # default response: nothin was found
    return {}

db = SQLAlchemy(api)

class NewsBulletin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<newsbreak {self.id}: {self.message} ({self.source})>'

db.create_all()

@api.route('/newsbreak', methods=['GET'])
def get_newsbreak():
    bulletin = NewsBulletin.query.all()
    return jsonify([newsbreak.__repr__() for newsbreak in bulletin])

@api.route('/newsbreak/<int:newsbreak_id>', methods=['GET'])
def get_newsbreak(newsbreak_id):
    bulletin = NewsBulletin.query.get(newsbreak_id)
    if bulletin is None:
        return jsonify({'message': 'newsbreak not found'})
    return jsonify(bulletin.__repr__())

@api.route('/newsbreak', methods=['POST'])
def create_newsbreak():
    message = request.json['message']
    source = request.json['source']
    bulletin = NewsBulletin(message=message, source=source)
    db.session.add(bulletin)
    db.session.commit()
    return jsonify(bulletin.__repr__()), 201

@api.route('/newsbreak/<int:newsbreak_id>', methods=['PUT'])
def update_newsbreak(newsbreak_id):
    bulletin = NewsBulletin.query.get(newsbreak_id)
    if bulletin is None:
        return jsonify({'message': 'newsbreak not found'})
    bulletin.message = request.json.get('message', bulletin.message)
    bulletin.source = request.json.get('source', bulletin.source)
    db.session.commit()
    return jsonify(bulletin.__repr__())

@api.route('/newsbreak/<int:newsbreak_id>', methods=['DELETE'])
def delete_newsbreak(newsbreak_id):
    bulletin = NewsBulletin.query.get(newsbreak_id)
    if bulletin is None:
        return jsonify({'message': 'newsbreak not found'})
    db.session.delete(bulletin)
    db.session.commit()
    return jsonify({'message': 'newsbreak deleted'})
