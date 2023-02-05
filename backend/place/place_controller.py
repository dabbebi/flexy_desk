from flask import Blueprint, request, jsonify
from app import db
from backend.middlewares.verify_login import login_required
from .place_model import Place, place_schema, places_schema
from marshmallow import ValidationError
import uuid # for public id

# Blueprint Configuration
place_bp = Blueprint('place_bp', __name__)

@place_bp.route('/place/book', methods=['POST'])
@login_required
def book_place(current_user):
    """_______________Book place________________"""
    try:
        body = request.json
        place = Place.query.filter(Place.user_id==current_user.public_id, Place.date==body["date"]).first()
        if not place:   
            new_place = Place(body)
            new_place.public_id = str(uuid.uuid4())
            new_place.firstname = current_user.firstname
            new_place.lastname = current_user.lastname
            new_place.user_id = current_user.public_id
            db.session.add(new_place)
            db.session.commit()
            places = Place.query.filter(Place.floor==body["floor"], Place.date==body["date"]).all()
            result = places_schema.dump(places)
            return jsonify(result), 200
        else:
            return {"message": "You have already booked a place"}, 400
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return {"error" : str(e)}, 500

@place_bp.route('/place/unbook', methods=['POST'])
@login_required
def unbook_place(current_user):
    """_______________Unbook place________________"""
    try:
        body = request.json
        place = Place.query.filter(Place.user_id==current_user.public_id, Place.date==body["date"]).first()
        if place:
            db.session.delete(place)
            db.session.commit()
            places = Place.query.filter(Place.floor==body["floor"], Place.date==body["date"]).all()
            result = places_schema.dump(places)
            return jsonify(result), 200
        else:
            return {"message": "You haven't booked any place in this date"}, 400
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return {"error" : str(e)}, 500

@place_bp.route('/place/officestatus', methods=['POST'])
@login_required
def get_office_status(current_user):
    """_______________Get office status________________"""
    try:
        body = request.json
        places = Place.query.filter(Place.floor==body["floor"], Place.date==body["date"]).all()
        result = places_schema.dump(places)
        return jsonify(result), 200
    except Exception as e:
        return {"error" : str(e)}, 500