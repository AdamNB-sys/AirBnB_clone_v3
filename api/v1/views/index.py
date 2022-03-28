#!/usr/bin/python3
"""index of flask routes"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def app_views_status():
    """returns status: ok if app is running"""
    return jsonify({'status': 'OK'})
