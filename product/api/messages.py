from flask import Blueprint
# Using Flask due its dependencies with MarkupSafe and ItsDangerous
# MarkupSafe comes with Jinja. It escapes untrusted input when rendering 
# templates to avoid injection attacks.
# ItsDangerous securely signs data to ensure its integrity. This is used
# to protect Flask’s session cookie.
from flask import Flask, render_template, url_for, request, redirect

api = Blueprint('messages',__name__,url_prefix='/messages')

@api.route('/fetch_categories', methods=['POST'])
def fetch_categories():
    if request.method == 'POST':
        msg = request.json
        user_token = msg['token']
        msg_categ = msg['categorie']
        start_date = msg['start_date']
        end_date = msg['end_date']

        print(f"user wants {request.json}")
    
    remove_later = [
        { 'summary' : 'hello', 'source':'https://google.com' },
        { 'summary' : 'this', 'source':'https://google.com' },
        { 'summary' : 'is in', 'source':'https://google.com' },
        { 'summary' : 'to-do', 'source':'https://google.com' },
        { 'summary' : 'for the', 'source':'https://google.com' },
        { 'summary' : 'categories,', 'source':'https://google.com' },
        { 'summary' : 'bye', 'source':'https://google.com' }]
    return remove_later

