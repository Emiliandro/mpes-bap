from flask import Blueprint
from flask import request
from api.model.basic_request import BasicRequest

import inspect

api = Blueprint('messages',__name__,url_prefix='/messages')

# check if values are valide for request
def basic_request_validations(basic_request):
    is_br = isinstance(basic_request,BasicRequest)
    return is_br

# check if token is valid, this is TBD
def token_validation(token):
    if isinstance(token,str) == False:
        return False
    return True

@api.route('/fetch', methods=['POST'])
def fetch_categories():
    if request.method == 'POST':
        msg = request.json
        
        user_token = msg['token']
        msg_categ = msg['categorie']
        start_date = msg['start_date']
        end_date = msg['end_date']

        basic_request = BasicRequest(token=user_token,categorie=msg_categ,start_time=start_date,end_time=end_date)
        
        if (basic_request_validations(basic_request)):
            print(f"user wants {basic_request}")
    
    # default response: nothin was found
    return {}