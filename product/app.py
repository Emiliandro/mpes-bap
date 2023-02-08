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
from demonstration import app as demonstration
from api.messages import api

from flask import Blueprint
title = "Bem vindo ao Bap 🤖"

# MISC -----------------


def create_app():
    # Using Flask due its dependencies with MarkupSafe and ItsDangerous
    # MarkupSafe comes with Jinja. It escapes untrusted input when rendering 
    # templates to avoid injection attacks.
    # ItsDangerous securely signs data to ensure its integrity. This is used
    # to protect Flask’s session cookie.
    app = Flask(__name__)
    app.register_blueprint(demonstration)
    app.register_blueprint(api)
    return app

app = create_app()

if (__name__ == "__main__"):
    app.run(debug=True)
