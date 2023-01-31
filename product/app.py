from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.RawImportsDB import RawImportsDB as riDB
from utils.NonRepudiationDB import NonRepudiationDB as nrDB
from utils.NonRepudiationDB import Nonr
from utils.CachedMessagesDB import CachedMessagesDB as cmDB

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

raw_imports = ri_helper.getAll()
non_repudiations = nr_helper.getAll()

#  regarding cyber security non repudiation, this assures that the sender of
#  information is provided with proof of delivery and the recipient is provided
#  with proof of the sender's request made, so neither can later deny having
#  processed the information throw the field "Suas ultimas buscas".
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_nr = Nonr(summary=task_content)
        try:
            nr_helper.append(new_nr)
            return redirect('/')
        except:
            return 'error adding value'
    else:
        raw_imports = ri_helper.getAll()
        non_repudiations = nr_helper.getAll()

    title = "Bem vindo ao Bap 🤖"
    return render_template('demonstration.html',title=title, non_repudiations=non_repudiations,raw_imports=raw_imports)

if (__name__ == "__main__"):
    app.run(debug=True)