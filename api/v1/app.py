#!/usr/bin/python3
"""Script to start the api"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(exception):
    """closes application"""
    storage.close()


if __name__ == "__main__":
    """script not run on import"""
    if environ.get('HBNB_API_HOST') is None:
        host = '0.0.0.0'
    else:
        host = environ.get('HBNB_API_HOST')

    if environ.get('HBNB_API_PORT') is None:
        port = '5000'
    else:
        port = environ.get('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
