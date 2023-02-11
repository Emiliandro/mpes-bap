from flask import Flask, Blueprint, request, jsonify
from datetime import datetime
from markupsafe import escape
from demonstration import app as demonstration
from BulletinDB import BulletinDB, NewsBulletin

def create_app():
    app = Flask(__name__)
    app.register_blueprint(demonstration)
    return app

app = create_app()
bulletin_helper = BulletinDB()

def default_answer():
    return jsonify({})

def formatted_request_validations(formatted_request):
#    is_br = isinstance(formatted_request,BasicRequest)
    return True

def token_validation(token):
    if isinstance(token,str) == False:
        return False
    return True

def create_request_model(msg):
    return {
        'token':escape(msg['token']),
        'categorie':escape(msg['categorie']),
        'start_time':escape(msg['start_date']),
        'end_time':escape(msg['end_date'])
    }

def create_request_news(msg):
    return {
        'token':escape(msg['token']),
        'title':escape(msg['title']),
        'message':escape(msg['message']),
        'categorie':escape(msg['categorie']).lower(),
        'source':escape(msg['source']),
        'date_created':escape(msg['date_created'])
    }

@app.route('/bap/categorie', methods=['POST'])
def get_newsbreak():
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_model(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()
    
    bulletin = bulletin_helper.getCategorie(formatted_request['categorie'])
    if bulletin is None:
        return jsonify({'message': 'categorie not found'})
    return jsonify(bulletin.__repr__())

@app.route('/bap/fetch', methods=['POST'])
def getall_newsbreak():
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_model(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()

    bulletin = bulletin_helper.getAll()
    return jsonify([news.__repr__() for news in bulletin])

@app.route('/bap/add', methods=['POST'])
def create_newsbreak():
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_news(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()
    
    return bulletin_helper.createAndAppend(formatted_request=formatted_request)


@app.route('/bap/<url>', methods=['POST'])
def delete_newsbreak(newsbreak_id):
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_model(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()

    return bulletin_helper.remove(value=formatted_request['source'])

    # return jsonify({'message': 'newsbreak deleted'})

if (__name__ == "__main__"):
    app.run(debug=True)
