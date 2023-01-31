from flask import Flask, render_template, url_for, request, redirect
from utils.RawImportsDB import RawImportsDB as riDB
from utils.RawImportsDB import Raw
from utils.NonRepudiationDB import NonRepudiationDB as nrDB
from utils.NonRepudiationDB import Nonr
from utils.CachedMessagesDB import CachedMessagesDB as cmDB
from utils.FeedManager import get_if_contain, get_categories, RawMessage

# Using Flask due its dependencies with MarkupSafe and ItsDangerous
# MarkupSafe comes with Jinja. It escapes untrusted input when rendering 
# templates to avoid injection attacks.
# ItsDangerous securely signs data to ensure its integrity. This is used
# to protect Flask’s session cookie.
app = Flask(__name__)

# Raw Imports DB contain every message filtered by the Webscrapping and the Feedreader
ri_helper = riDB()

# Non Repudiation DB contain the history of requests made be the api
nr_helper = nrDB()

# Cached Messages DB contain all messages approved to be sent by the api
cm_helper = cmDB()


# DEMONSTRATION ----------------------------------

list_results = []
feed_categories = get_categories()
for feed in feed_categories:
    feed_results = get_if_contain(feed)
    for result in feed_results:
        value = Raw(categorie=result.tag,summary=result.summary,source=result.url)
        list_results.append(value)

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
        return do_update_nonR(request)
    else:
        raw_imports = ri_helper.getAll()
        non_repudiations = nr_helper.getAll()

    title = "Bem vindo ao Bap 🤖"
    return render_template('demonstration.html',title=title, non_repudiations=non_repudiations,raw_imports=raw_imports)

def do_update_nonR(request):
    task_content = request.form['content']
    new_nr = Nonr(summary=task_content)
    try:
        nr_helper.append(new_nr)
        return redirect('/')
    except:
        return 'error adding value'

# REST API for Cached Messages ---------------------
@app.route('/get_cached', methods=['GET'])
def get_all_cached_messages():
    remove_later = [
        { 'summary' : 'hello', 'source':'https://google.com' },
        { 'summary' : 'this', 'source':'https://google.com' },
        { 'summary' : 'is in', 'source':'https://google.com' },
        { 'summary' : 'to-do,', 'source':'https://google.com' },
        { 'summary' : 'bye', 'source':'https://google.com' }]
    return remove_later


@app.route('/get_categorie', methods=['POST', 'GET'])
def get_categorie_cached_messages():
    if request.method == 'POST':
        interest = request.form['content']
        print(f"user wants {interest}")
    
    remove_later = [
        { 'summary' : 'hello', 'source':'https://google.com' },
        { 'summary' : 'this', 'source':'https://google.com' },
        { 'summary' : 'is in', 'source':'https://google.com' },
        { 'summary' : 'to-do', 'source':'https://google.com' },
        { 'summary' : 'for the', 'source':'https://google.com' },
        { 'summary' : 'categories,', 'source':'https://google.com' },
        { 'summary' : 'bye', 'source':'https://google.com' }]
    return remove_later

# MISC ---------------------------------------------

if (__name__ == "__main__"):
    app.run(debug=True)