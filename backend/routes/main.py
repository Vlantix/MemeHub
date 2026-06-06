from flask import Blueprint, jsonify

landing_bp = Blueprint('landing', __name__)

@landing_bp.route("/")
def index():
    return jsonify({"message": "MemeHub API is running"}), 200