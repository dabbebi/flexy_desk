from backend.authentication.validation.login_validator import login_validator
from flask import Blueprint, request, jsonify, current_app as app
import jwt
import datetime
from marshmallow import ValidationError
from backend.middlewares.verify_login import refresh_token_required
from backend.user.user_model import User
import uuid
from app import db 

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """____________________Login______________________"""
    try:
        body = login_validator.load(request.json)
        email = body['email']
        password = body['password']
        if(email == '' or password == ''):
            return {'error' : 'Invalid body request!'}, 400
        user = User.query.filter(User.email==email).first()
        if not user:
            user = User(body)
            user.public_id = str(uuid.uuid4())
            user.privilege = 'User'
            user.firstname = email[0].upper() + email[1: email.index('.')].lower()
            user.lastname = email[email.index('.') + 1].upper() + email[email.index('.') + 2 : email.index('@')].lower()
            user.username = user.firstname[0] + user.lastname
            db.session.add(user)
            db.session.commit()
        else:
            if user.password != password:
                return {'password': ['Password is incorrect !']}, 401
        result = {
        'access_token': jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=43200)}, app.config['SECRET_KEY'], algorithm='HS256'),
        'refresh_token': jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=432000)}, app.config['SECRET_KEY'], algorithm='HS256')
        }
        return jsonify(result), 200  
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return {"error" : str(e)}, 500

@auth_bp.route('/refresh', methods=['POST'])
@refresh_token_required
def refresh(current_user):
    """____________________Refresh______________________"""
    result = {
        'access_token': jwt.encode({'public_id': current_user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=43200)}, app.config['SECRET_KEY'], algorithm='HS256'),
    }
    return jsonify(result), 200