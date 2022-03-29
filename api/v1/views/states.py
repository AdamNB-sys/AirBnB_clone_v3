#!/usr/bin/python3
"""view for state to handle all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask.views import View
import json
from models.state import State
from models import storage


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


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_state():
    """retrieves all instances of a state"""
    all_state = storage.all(State).values()
    state_list = []
    for state in all_state:
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state_by_id(state_id):
    """retrieves state by object id"""
    got_state = storage.get(State, state_id)
    if got_state is None:
        return jsonify({"error": "Not found"}), 404
    else:
        return jsonify(got_state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state_by_id(state_id):
    """retrieves state by object id"""
    got_state = storage.get(State, state_id)
    # print(got_state)
    if got_state is None:
        return jsonify({"error": "Not found"}), 404
    else:
        storage.delete(got_state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """creates an instance of a state"""
    content = request.get_json(silent=True)
    # print(content)
    dumped = json.dumps(content)
    # print(type(json.dumps(content)))
    # print(is_json(content))
    # print(is_json(dumped))
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")
    # print(content.keys())
    if content.get("name") is None:
        abort(400, "Missing name")

    new_state = State(**content)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """updates an instance of a state"""
    content = request.get_json(silent=True)
    dumped = json.dumps(content)
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")
    if storage.get(State, state_id) is None:
        abort(404)

    if content.get("created_at"):
        del content["created_at"]
    if content.get("updated_at"):
        del content["updated_at"]
    if content.get("id"):
        del content["id"]

    if content.get("name") is None:
        abort(400, "Missing name")

    this_state = storage.get(State, state_id)
    this_state.update(**content)
    return jsonify(this_state.to_dict()), 200
