from flask import Blueprint
# Using Flask due its dependencies with MarkupSafe and ItsDangerous
# MarkupSafe comes with Jinja. It escapes untrusted input when rendering 
# templates to avoid injection attacks.
# ItsDangerous securely signs data to ensure its integrity. This is used
# to protect Flask’s session cookie.
from flask import Flask, render_template, url_for, request, redirect

# escape function causes param to be rendered as text, preventing the execution of 
# injection script in the user’s browser or the in the api request.
from markupsafe import escape

# using duckduckgo_search, because DuckDuckGo does not collect or share personal
# information. That its privacy policy, it prevents search leakage by default.  
# read more about it at https://duckduckgo.com/privacy
from duckduckgo_search import ddg_suggestions, ddg

from utils.RawImportsDB import RawImportsDB as riDB
from utils.RawImportsDB import Raw
from utils.NonRepudiationDB import NonRepudiationDB as nrDB
from utils.NonRepudiationDB import Nonr
from utils.CachedMessagesDB import CachedMessagesDB as cmDB
from utils.CachedMessagesDB import Cachedm
from utils.FeedManager import get_if_contain, get_categories, RawMessage

title = "Bem vindo ao Bap 🤖"

# Using Flask due its dependencies with MarkupSafe and ItsDangerous
# MarkupSafe comes with Jinja. It escapes untrusted input when rendering 
# templates to avoid injection attacks.
# ItsDangerous securely signs data to ensure its integrity. This is used
# to protect Flask’s session cookie.
app = Blueprint('demonstration',__name__,url_prefix='/demo')

# Raw Imports DB contain every message filtered by the Webscrapping and the Feedreader
ri_helper = riDB()

# Non Repudiation DB contain the history of requests made be the api
nr_helper = nrDB()

# Cached Messages DB contain all messages approved to be sent by the api
cm_helper = cmDB()


# DEMONSTRATION ----------------------------------

list_suggestions = []
list_results = []
feed_categories = get_categories()
for feed in feed_categories:
    feed_results = get_if_contain(feed)
    for result in feed_results:
        value = Raw(categorie=result.tag,summary=result.summary,source=result.url)
        list_results.append(value)

# using duckduckgo_search, because DuckDuckGo does not collect or share personal
# information. That its privacy policy, it prevents search leakage by default.  
# read more about it at https://duckduckgo.com/privacy
for feed in feed_categories:
    results = ddg_suggestions(feed,region='br-pt')
    for result in results:    
        list_suggestions.append(result['phrase'])

ri_helper.appendList(list_results)

raw_imports = ri_helper.getAll()
non_repudiations = nr_helper.getAll()

#  Regarding cyber security non repudiation, this assures that the sender of
#  information is provided with proof of delivery and the recipient is provided
#  with proof of the sender's request made, so neither can later deny having
#  processed the information throw the field "Suas ultimas buscas".
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return do_update_nonR(request.form['content'])
    else:
        raw_imports = ri_helper.getAll()
        non_repudiations = nr_helper.getAll()

    return render_template('demonstration.html',title=title, non_repudiations=non_repudiations,raw_imports=raw_imports,suggestions=list_suggestions,phrases=[])

def do_update_nonR(research):
    new_nr = Nonr(summary=research)
    try:
        nr_helper.append(new_nr)
        return redirect('/')
    except:
        return 'error adding value'

# SEARCH_ENGINE -----------------

# using duckduckgo_search, because DuckDuckGo does not collect or share personal
# information. That its privacy policy, it prevents search leakage by default.  
# read more about it at https://duckduckgo.com/privacy

def phrase_to_search(value):
    phrase_to_results = ddg(value, region='br-pt', safesearch='on', time='y')

    for phrase in phrase_to_results:
        cached_msg = Cachedm(body=phrase['body'],title=phrase['title'],source=phrase['href'],categorie="none")

    return phrase_to_results

@app.route('/phrase/<phrase>')
def search_for(phrase):
    # escape function causes param to be rendered as text, preventing the execution of 
    # injection script in the user’s browser or the in the api request.
    do_update_nonR(f"{escape(phrase)}")
    raw_imports = ri_helper.getAll()
    non_repudiations = nr_helper.getAll()

    # escape function causes param to be rendered as text, preventing the execution of 
    # injection script in the user’s browser or the in the api request.
    phrases = phrase_to_search(f"{escape(phrase)}")
    return render_template('demonstration.html',title=title, non_repudiations=non_repudiations,raw_imports=raw_imports,suggestions=list_suggestions,phrases=phrases)
