#!/usr/bin/python3
"""view for amenities to handle all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask.views import View
import json
from models.user import User
from models import storage
unallowed_update_keys = ["updated_at", "created_at", "id", "email"]


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


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_all_users():
    """retrieves all instances of users"""
    all_users = storage.all(User).values()
    user_list = []
    for user in all_users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user_by_id(user_id):
    """retrieves user by user id"""
    got_user = storage.get(User, user_id)
    if got_user is None:
        return jsonify({"error": "Not found"}), 404
    else:
        return jsonify(got_user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user_by_id(user_id):
    """deletes user by object id"""
    got_user = storage.get(User, user_id)
    # print(got_user)
    if got_user is None:
        return jsonify({"error": "Not found"}), 404
    else:
        storage.delete(got_user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """creates an instance of a user"""
    content = request.get_json(silent=True)
    # print(content)
    dumped = json.dumps(content)
    # print(type(json.dumps(content)))
    # print(is_json(content))
    # print(is_json(dumped))
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")
    # print(content.keys())
    if content.get("email") is None:
        abort(400, "Missing email")
    if content.get("password") is None:
        abort(400, "Missing password")

    new_user = User(**content)
    # storage.new(new_amenity)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """updates an instance of a user"""
    content = request.get_json(silent=True)
    dumped = json.dumps(content)
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")
    if storage.get(User, user_id) is None:
        abort(404)

    for nokey in unallowed_update_keys:
        if content.get(nokey):
            del content[nokey]

    this_user = storage.get(User, user_id)
    this_user.update(**content)
    return jsonify(this_user.to_dict()), 200
