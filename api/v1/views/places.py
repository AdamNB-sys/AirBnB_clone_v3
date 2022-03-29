#!/usr/bin/python3
"""view for places to handle all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask.views import View
import json
from models.city import City
from models.place import Place
from models.user import User
from models import storage
unallowed_update_keys = [
    "updated_at", "created_at", "id", "user_id", "city_id"]


def is_json(myjson):
    """returns bool if item is valid json"""
    if type(myjson) == str:
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True
    else:
        try:
            json.loads(str(myjson))
        except ValueError as e:
            return False
        return True


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_all_places(city_id):
    """retrieves all instances of places"""
    if storage.get(City, city_id) is None:
        abort(404)
    all_places = storage.all(Place).values()
    place_list = []
    for place in all_places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place_by_id(place_id):
    """retrieves place by place id"""
    got_place = storage.get(Place, place_id)
    if got_place is None:
        return jsonify({"error": "Not found"}), 404
    else:
        return jsonify(got_place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_by_id(place_id):
    """deletes place by object id"""
    got_place = storage.get(Place, place_id)
    # print(got_place)
    if got_place is None:
        return jsonify({"error": "Not found"}), 404
    else:
        storage.delete(got_place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """creates an instance of a place"""
    if storage.get(City, city_id) is None:
        abort(404)
    content = request.get_json(silent=True)
    # print(content)
    dumped = json.dumps(content)
    # print(type(json.dumps(content)))
    # print(is_json(content))
    # print(is_json(dumped))
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")
    # print(content.keys())

    if content.get("user_id") is None:
        abort(400, "Missing user_id")
    content['city_id'] = city_id
    if storage.get(User, content.get("user_id")) is None:
        abort(404)
    if content.get("name") is None:
        abort(400, "Missing name")

    new_place = Place(**content)
    # storage.new(new_amenity)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """updates an instance of a place"""
    if storage.get(Place, place_id) is None:
        abort(404)
    content = request.get_json(silent=True)
    dumped = json.dumps(content)
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")

    for nokey in unallowed_update_keys:
        if content.get(nokey):
            del content[nokey]

    this_place = storage.get(Place, place_id)
    this_place.update(**content)
    return jsonify(this_place.to_dict()), 200
