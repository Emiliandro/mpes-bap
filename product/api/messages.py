from flask import Blueprint
from flask import request
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