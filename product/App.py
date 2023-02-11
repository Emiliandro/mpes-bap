from flask import Flask, Blueprint, request, jsonify
from datetime import datetime
from datetime import date as datetime_date
from markupsafe import escape
from demonstration import app as demonstration
from BulletinDB import BulletinDB

def create_app():
    app = Flask(__name__)
    app.register_blueprint(demonstration)
    return app

app = create_app()
bulletin_helper = BulletinDB()

def default_answer():
    return jsonify({})

def is_list_of_strings(lst):
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False

def formatted_request_validations(formatted_request):
    if "categories" in formatted_request:
        if is_list_of_strings(formatted_request['categories']) == False:
            return False
    else:
        if isinstance(formatted_request['categorie'],str) == False:
            print("categorie invalid", type(formatted_request['categorie']))
            return False

    if "date_created" in formatted_request:
        if isinstance(formatted_request['date_created'],datetime_date) == False:
            print("date_created invalid", type(formatted_request['date_created']))
            return False
        if isinstance(formatted_request['title'],str) == False:
            print("title invalid", type(formatted_request['title']))
            return False
        if isinstance(formatted_request['message'],str) == False:
            print("message invalid", type(formatted_request['message']))
            return False
        if isinstance(formatted_request['source'],str) == False:
            print("source invalid", type(formatted_request['source']))
            return False
    else:
        if isinstance(formatted_request['start_date'],datetime_date) == False:
            print("start_date invalid", type(formatted_request['start_date']))
            return False
        if isinstance(formatted_request['end_date'],datetime_date) == False:
            print("end_date invalid", type(formatted_request['end_date']))
            return False

    return True

def token_validation(token):
    if isinstance(token,str) == False:
        return False
    return True

def create_request_model(msg):
    return {
        'token':escape(msg['token']),
        'categorie':escape(msg['categorie']),
        'start_date':datetime.strptime(escape(msg['start_date']), '%m-%d-%Y').date(),
        'end_date':datetime.strptime(escape(msg['end_date']), '%m-%d-%Y').date()
    }

def create_request_model_categories(msg):
    return {
        'token':escape(msg['token']),
        'categories': (escape(elem) for elem in msg['categories']),
        'start_date':datetime.strptime(escape(msg['start_date']), '%m-%d-%Y').date(),
        'end_date':datetime.strptime(escape(msg['end_date']), '%m-%d-%Y').date()
    }

def create_request_news(msg):
    return {
        'token':escape(msg['token']),
        'title':escape(msg['title']),
        'message':escape(msg['message']),
        'categorie':escape(msg['categorie']).lower(),
        'source':escape(msg['source']),
        'date_created':datetime.strptime(escape(msg['date_created']), '%m-%d-%Y').date()
    }

@app.route('/bap/categorie', methods=['POST'])
def get_categorie():
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

@app.route('/bap/categories', methods=['POST'])
def get_categories():
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_model_categories(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()
    
    bulletin = bulletin_helper.getCategories(formatted_request['categories'])
    if bulletin is None:
        return jsonify({'message': 'categories not found'})
    return jsonify(bulletin.__repr__())


@app.route('/bap/fetch', methods=['POST'])
def fetch_all():
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_model(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()

    return bulletin_helper.getAll()

@app.route('/bap/add', methods=['POST'])
def add():
    if request.method != 'POST':
        return default_answer()
    
    msg = request.json
    formatted_request = create_request_news(msg=msg)

    if formatted_request_validations(formatted_request) == False:
        return default_answer()
    
    return bulletin_helper.createAndAppend(formatted_request=formatted_request)

@app.route('/bap/remove', methods=['POST'])
def remove():
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
