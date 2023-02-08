from flask import Flask
from demonstration import app as demonstration
from api.messages import api

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
