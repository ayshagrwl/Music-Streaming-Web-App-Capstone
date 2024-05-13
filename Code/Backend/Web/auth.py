from flask import Blueprint
from flask_restful import Resource, reqparse, abort, fields, marshal_with, Api
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User 
from .packages import db
from datetime import datetime


auth = Blueprint('auth',__name__)

signup_parser = reqparse.RequestParser()
signup_parser.add_argument("name", type=str, help="Name of the user is required", required=True)
signup_parser.add_argument("password", type=str, help="Password is required", required=True)
signup_parser.add_argument("email", type=str, help="Email of the user is required", required=True)

user_fields = {
    "user_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "token": fields.String,
    "role": fields.String}

class SignUp (Resource):

    @marshal_with(user_fields)
    def post(self):
        req_args = signup_parser.parse_args()
        name = req_args["name"]
        password = req_args["password"]
        email = req_args["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            abort(403, message="User already exist")
        else:
            new_user = User(email = email, name = name, password = generate_password_hash(password, method='scrypt'),role='user')
            db.session.add(new_user)
            db.session.commit()
            # Generate access token for the new user
            access_token = create_access_token(identity=new_user.user_id )
            # Return user and access token as response
            response = {"user_id": new_user.user_id, "name": new_user.name, "email": new_user.email, "token": access_token, "role": 'user'}
            return response, 200



login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, help='This field cannot be blank', required=True)
login_parser.add_argument('password', type=str, help='This field cannot be blank', required=True)

login_fields = {"user_id": fields.Integer, "token": fields.String, "role": fields.String}

class Login(Resource):
    @marshal_with(login_fields)
    def post(self):
        req_args = login_parser.parse_args()
        email = req_args["email"]
        password = req_args["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                user.last_login = datetime.utcnow()
                db.session.commit()
                access_token = create_access_token(identity=user.user_id)
                response = {"user_id": user.user_id, "token": access_token, "role": user.role}
                return response, 200
            else:
                abort(401, message="Wrong password")
        else:
            abort(401, message="User does not exist")

admin_login_parser = reqparse.RequestParser()
admin_login_parser.add_argument("email", type=str, help="this field can not be empty", required=True)
admin_login_parser.add_argument("password",type=str, help="This field can not be empty", required=True)

admin_fields = {"user_id":fields.Integer, "token":fields.String, "role":fields.String}

class Admin_login(Resource):
    @marshal_with(admin_fields)
    def post(self):
        req_args = admin_login_parser.parse_args()
        email = req_args["email"]
        password = req_args["password"]
        user = User.query.filter_by(email=email).first()
        if user.role=='admin':
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.user_id)
                response = {"user_id":user.user_id, "token":access_token, "role": user.role}
                return response, 200
            else:
                abort(401, message="Wrong password")
        else:
            abort(401, message="Wrong credentials")


class ToggleCreator(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        user.role = 'creator'
        db.session.commit()
        print(user.role)

        return {"message": f"Creator status toggled. Please relogin to load dashboard "}, 200



# Blacklist is used to store the tokens that are logged out
blacklist = set()

class Logout (Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        # print(jti)
        blacklist.add(jti)
        # print(blacklist)
        return {"message": "Successfully logged out"}, 200

