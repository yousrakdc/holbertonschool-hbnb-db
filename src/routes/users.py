"""This module contains the routes for the users endpoints."""


from flask import Blueprint, request, jsonify
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User
from src import bcrypt
from functools import wraps
from src.persistence import db

# Custom decorator to check user permissions
def check_user_permission(func):
    @wraps(func)
    @jwt_required()
    def decorated_function(user_id, *args, **kwargs):
        current_user = get_jwt_identity()
        user = db.get('user', user_id)  # Retrieve user by ID

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Check if the current user is authorized to access this resource
        if current_user != user.id:
            return jsonify({"msg": "Unauthorized"}), 401

        # If authorized, execute the function
        return func(user_id, *args, **kwargs)

    return decorated_function

users_bp = Blueprint("users", __name__, url_prefix="/users")

users_bp.route("/", methods=["GET"])(get_users)
users_bp.route("/", methods=["POST"])(create_user)

users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)
users_bp.route("/<user_id>", methods=["PUT"])(update_user)
users_bp.route("/<user_id>", methods=["DELETE"])(delete_user)

@users_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity={'email': user.email, 'is_admin': user.is_admin})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Wrong email or password"}), 401

# Example of a protected route
@users_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200