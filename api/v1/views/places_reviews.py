#!/usr/bin/python3
"""view for places to handle all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask.views import View
import json
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
unallowed_update_keys = [
    "updated_at", "created_at", "id", "user_id", "place_id"]


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


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_all_reviews_by_place(place_id):
    """retrieves all instances of place reviews"""
    if storage.get(Place, place_id) is None:
        abort(404)
    all_reviews = storage.all(Review).values()
    review_list = []
    for review in all_reviews:
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review_by_review_id(review_id):
    """retrieves a review by review id"""
    got_review = storage.get(Review, review_id)
    if got_review is None:
        return jsonify({"error": "Not found"}), 404
    else:
        return jsonify(got_review.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review_by_review_id(review_id):
    """deletes review by review id"""
    got_review = storage.get(Review, review_id)
    # print(got_place)
    if got_review is None:
        return jsonify({"error": "Not found"}), 404
    else:
        storage.delete(got_review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review_by_place_id(place_id):
    """creates an instance of a review"""
    if storage.get(Place, place_id) is None:
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
    content['place_id'] = place_id
    if storage.get(User, content.get("user_id")) is None:
        abort(404)
    if content.get("text") is None:
        abort(400, "Missing text")

    new_review = Review(**content)
    # storage.new(new_amenity)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review_by_review_id(review_id):
    """updates an instance of a place"""
    if storage.get(Review, review_id) is None:
        abort(404)
    content = request.get_json(silent=True)
    dumped = json.dumps(content)
    if content is None or is_json(dumped) is False:
        abort(400, "Not a JSON")

    for nokey in unallowed_update_keys:
        if content.get(nokey):
            del content[nokey]

    this_review = storage.get(Review, review_id)
    this_review.update(**content)
    return jsonify(this_review.to_dict()), 200
