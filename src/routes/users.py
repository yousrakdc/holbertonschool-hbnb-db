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
from src.persistence.db import DBRepository

# Initialize the DBRepository as 'db'
db = DBRepository()

# Custom decorator to check user permissions
def check_user_permission(func):
    @wraps(func)
    @jwt_required()
    def decorated_function(user_id, *args, **kwargs):
        current_user_id = get_jwt_identity()  # Get the identity of the current user from the JWT
        user = db.get('user', user_id)  # Retrieve the user by ID from the database

        if not user:
            return jsonify({"msg": "User not found"}), 404  # Return 404 if user not found

        # Check if the current user is authorized to access this resource
        if current_user_id != user.id:
            return jsonify({"msg": "Unauthorized"}), 401  # Return 401 if user is not authorized

        # If authorized, execute the function
        return func(user_id, *args, **kwargs)

    return decorated_function

# Create a Blueprint for the users module
users_bp = Blueprint("users", __name__, url_prefix="/users")

# Define routes for the users endpoint
users_bp.route("/", methods=["GET"])(get_users)  # Route to get all users
users_bp.route("/", methods=["POST"])(create_user)  # Route to create a new user

users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)  # Route to get a user by ID
users_bp.route("/<user_id>", methods=["PUT"])(jwt_required()(check_user_permission(update_user)))  # Route to update a user by ID with permission check
users_bp.route("/<user_id>", methods=["DELETE"])(jwt_required()(check_user_permission(delete_user)))  # Route to delete a user by ID with permission check

@users_bp.route('/login', methods=['POST'])
def login():
    # Extract email and password from the request body
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400  # Return 400 if email or password is missing

    # Get the user by email from the database
    user = db.get_by_email(email)
    if user and bcrypt.check_password_hash(user.password_hash, password):
        # If the user is found and the password matches, create an access token
        access_token = create_access_token(identity=user.id)  # Use user ID as the token identity
        return jsonify(access_token=access_token), 200  # Return the access token

    return jsonify({"msg": "Wrong email or password"}), 401  # Return 401 if email or password is incorrect

# Example of a protected route
@users_bp.route('/protected', methods=['GET'])
@jwt_required()  # JWT is required to access this route
def protected():
    current_user_id = get_jwt_identity()  # Get the identity of the current user from the JWT
    user = db.get('user', current_user_id)  # Retrieve the user by ID from the database

    if user:
        return jsonify(logged_in_as=user.email), 200  # Return the current user's email
    return jsonify({"msg": "User not found"}), 404  # Return 404 if user not found

# Example of an admin-protected route
@users_bp.route('/admin', methods=['GET'])
@jwt_required()  # JWT is required to access this route
def admin_protected():
    current_user_id = get_jwt_identity()  # Get the identity of the current user from the JWT
    user = db.get('user', current_user_id)  # Retrieve the user by ID from the database

    if user and user.is_admin:
        return jsonify(message="Admin protected endpoint"), 200  # Return a message if the user is an admin
    else:
        return jsonify(message="Admin access required"), 403  # Return 403 if the user is not an admin
