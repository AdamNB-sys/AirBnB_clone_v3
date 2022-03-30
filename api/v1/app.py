#!/usr/bin/python3
"""Script to start the api"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import environ

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(exception):
    """closes application"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({"error": "Not found"}), 404


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

    app.run(debug=True, host=host, port=port, threaded=True)
