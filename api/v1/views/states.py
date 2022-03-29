#!/usr/bin/python3
"""view for state to handle all default RESTful API actions"""
# creates a state: POST /api/v1/states
# You must use request.get_json from Flask to transform the HTTP body request to a dictionary
# If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
# If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
# Returns the new State with the status code 201
# updates a state object: PUT /api/v1/states/<state_id>
# If the state_id is not linked to any State object, raise a 404 error
# You must use request.get_json from Flask to transform the HTTP body request to a dictionary
# If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
# Update the State object with all key-value pairs of the dictionary.
# Ignore keys: id, created_at and updated_at
# Returns the State object with the status code 200
from api.v1.views import app_views
from flask import jsonify
from flask.views import View
from models.state import State
from models import storage


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
    print(got_state)
    if got_state is None:
        return jsonify({"error": "Not found"}), 404
    else:
        storage.delete(got_state)
        storage.save()
        return jsonify({}), 200
