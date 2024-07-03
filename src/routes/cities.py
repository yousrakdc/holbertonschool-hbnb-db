from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

cities_bp.route("/", methods=["GET"])(get_cities)
cities_bp.route("/", methods=["POST"])(jwt_required()(create_city))

cities_bp.route("/<city_id>", methods=["GET"])(get_city_by_id)
cities_bp.route("/<city_id>", methods=["PUT"])(jwt_required()(update_city))
cities_bp.route("/<city_id>", methods=["DELETE"])(jwt_required()(delete_city))