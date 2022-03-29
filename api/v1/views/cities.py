#!/usr/bin/python3
"""view for city to handle all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask.views import View
import json
from models.city import City
from models.state import State
from models import storage
unallowed_update_keys = ["updated_at", "created_at", "id", "state_id"]


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


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_all_state_cities(state_id):
    """retrieves all instances of cities in a state"""
    if storage.get(State, state_id) is None:
        abort(404)
    all_cities = storage.all(City).values()
    city_list = []
    for city in all_cities:
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city_by_id(city_id):
    """retrieves city by object id"""
    got_city = storage.get(City, city_id)
    if got_city is None:
        abort(404)
    else:
        return jsonify(got_city.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city_by_id(city_id):
    """retrieves state by object id"""
    got_city = storage.get(City, city_id)
    # print(got_city)
    if got_city is None:
        abort(404)
    else:
        storage.delete(got_city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """creates an instance of a city"""
    if storage.get(State, state_id) is None:
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
    content['state_id'] = state_id
    if content.get("name") is None:
        abort(400, "Missing name")

    new_city = City(**content)
    storage.new(new_city)
    storage.save()
    # print(new_city.to_dict())
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """updates an instance of a city"""
    if storage.get(City, city_id) is None:
        abort(404)
    content = request.get_json(silent=True)
    dumped = json.dumps(content)
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")

    for nokey in unallowed_update_keys:
        if content.get(nokey):
            del content[nokey]

    this_city = storage.get(City, city_id)
    this_city.update(**content)
    return jsonify(this_city.to_dict()), 200
