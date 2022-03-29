#!/usr/bin/python3
"""view for amenities to handle all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask.views import View
import json
from models.amenity import Amenity
from models import storage
unallowed_update_keys = ["updated_at", "created_at", "id"]


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


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """retrieves all instances of amenities"""
    all_amenities = storage.all(Amenity).values()
    amenity_list = []
    for amenity in all_amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity_by_id(amenity_id):
    """retrieves amenity by object id"""
    got_amenity = storage.get(Amenity, amenity_id)
    if got_amenity is None:
        return jsonify({"error": "Not found"}), 404
    else:
        return jsonify(got_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """deletes amenity by object id"""
    got_amenity = storage.get(Amenity, amenity_id)
    # print(got_amenity)
    if got_amenity is None:
        return jsonify({"error": "Not found"}), 404
    else:
        storage.delete(got_amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """creates an instance of an amenity"""
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

    new_amenity = Amenity(**content)
    # storage.new(new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """updates an instance of an amenity"""
    content = request.get_json(silent=True)
    dumped = json.dumps(content)
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")
    if storage.get(Amenity, amenity_id) is None:
        abort(404)

    for nokey in unallowed_update_keys:
        if content.get(nokey):
            del content[nokey]

    this_amenity = storage.get(Amenity, amenity_id)
    this_amenity.update(**content)
    return jsonify(this_amenity.to_dict()), 200
