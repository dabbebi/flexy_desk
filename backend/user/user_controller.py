from flask import Blueprint, request, jsonify
from app import db
from backend.middlewares.verify_login import login_required
from backend.user.validation.user_validator import update_user_password_validator, create_user_validator, update_user_validator
from .user_model import User, user_schema, users_schema
from marshmallow import ValidationError
import uuid # for public id

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/identity', methods=['GET'])
@login_required
def get_identity(current_user):
    """_______________Get identity________________"""
    try:
        return user_schema.jsonify(current_user)
    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user', methods=['POST'])
@login_required
def create_user(current_user):
    """_______________Create user________________"""
    try:
        body = create_user_validator.load(request.json)
        new_user = User(body)
        new_user.public_id = str(uuid.uuid4())
        new_user.username = body["firstname"][0] + body["lastname"]
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user', methods=['GET'])
@login_required
def get_all_users(current_user):
    """_______________Get all users________________"""
    try:
        all_users = User.query.all()
        res = []
        for user in all_users:
            if user.public_id != current_user.public_id :
                res.append(user)
        result = users_schema.dump(res)
        return jsonify(result)
    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user/<number_users>/<page>', methods=['GET'])
@login_required
def get_users_per_page(current_user, number_users, page):
    """_______________Get users per page________________"""
    try:
        all_users = User.query.all()
        res = []
        for user in all_users:
            if user.public_id != current_user.public_id :
                res.append(user)
        
        if(len(res) == 0):
            return {
                "users" : [],
                "page" : int(page),
                "nb_users" : 0
                }, 200

        if(len(res) <= (int(number_users) * int(page)) - int(number_users)):
            return {"message" : "page not found !"}, 404

        result = []
        
        for i in range((int(number_users) * int(page)) - int(number_users), min(int(number_users) * int(page), len(res))):
            result.append(res[i])
        output = {
            "users" : users_schema.dump(result),
            "page" : int(page),
            "nb_users" : len(res)
        }
        return jsonify(output), 200

    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user/<public_id>', methods=['GET'])
@login_required
def get_single_user(current_user, public_id):
    """_______________Get single user________________"""
    try:
        user = User.query.filter(User.public_id==public_id).first()
        if user:
            return user_schema.jsonify(user)
        return {"message" : "User with public_id " + public_id + " not found !"}, 404
    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user/<public_id>', methods=['DELETE'])
@login_required
def delete_single_user(current_user, public_id):
    """_______________Delete single user________________"""
    try:
        user = User.query.filter(User.public_id==public_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return user_schema.jsonify(user)
        return {"message" : "User with public_id " + public_id + " not found !"}, 404
    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user/<public_id>', methods=['PUT'])
@login_required
def update_user(current_user,public_id):
    """_______________Update user________________"""
    try:
        body = update_user_validator.load(request.json)
        user = User.query.filter(User.public_id==public_id).first()
        if user:
            user.firstname = body['firstname']
            user.lastname = body['lastname']
            user.privilege = body['privilege']
            db.session.add(user)
            db.session.commit()
            return user_schema.jsonify(user)
        return {"message" : "User with public_id " + public_id + " not found !"}, 404
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return {"error" : str(e)}, 500

@user_bp.route('/user/password', methods=['PUT'])
@login_required
def update_user_password(current_user):
    """_______________Update user password________________"""
    try:
        body = update_user_password_validator.load(request.json)
        user = User.query.filter(User.public_id==current_user.public_id).first()
        if user:
            if user.password != body['current_password']:
                return {'password': ['Password is incorrect !']}, 401
            user.password =  body['new_password']
            db.session.add(user)
            db.session.commit()
            return user_schema.jsonify(user)
        return {"message" : "User with public_id " + current_user.public_id + " not found !"}, 404
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return {"error" : str(e)}, 500