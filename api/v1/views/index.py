#!/usr/bin/python3
"""index of flask routes"""
from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
key_dict = {"Amenity":  "amenities", "City": "cities",
            "Place": "places", "Review": "reviews",
            "State": "states", "User": "users"}


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def app_views_status():
    """returns status: ok if app is running"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_app_stats():
    """retrieves the number of each object by type"""
    obj_count = {}
    for key, value in classes.items():
        obj_count[key_dict[key]] = storage.count(value)
    return jsonify(obj_count)
