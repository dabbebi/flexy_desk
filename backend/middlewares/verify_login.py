from flask import request, current_app as app
import jwt
from functools import wraps
from backend.user.user_model import User

def login_required(f):
    """____________________@login_required decorator______________________"""
    @wraps(f)
    def verify_login(*args, **kwargs):
        token = request.headers.get('access_token')
        if not token :
            return {'message' : "Access token is missing !"}, 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter(User.public_id == data['public_id']).first()
            if(not current_user):
                return {'message' : "User not found !"}, 404
            return f(current_user, *args, **kwargs)
        except:
            return {'message' : "Invalid access token !"}, 401
    return verify_login

def refresh_token_required(f):
    """____________________@refresh_required decorator______________________"""
    @wraps(f)
    def verify_refresh_token(*args, **kwargs):
        token = request.headers.get('refresh_token')
        if not token :
            return {'message' : "Refresh token is missing !"}, 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter(User.public_id == data['public_id']).first()
            if(not current_user):
                return {'message' : "User not found !"}, 404
            return f(current_user, *args, **kwargs)
        except:
            return {'message' : "Invalid refresh token !"}, 401
    return verify_refresh_token