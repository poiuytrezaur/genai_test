"""Authentication routes for user login, registration, and logout."""

from __future__ import annotations

import logging
from typing import Any

from flask import Blueprint, jsonify, request, session

from backend.services import AuthService

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Constants for validation
MIN_USERNAME_LENGTH = 5
MAX_USERNAME_LENGTH = 25
MIN_PASSWORD_LENGTH = 6


@auth_bp.route("/register", methods=["POST"])
def register() -> tuple[Any, int]:  # noqa: PLR0911
    """Register a new user.

    Expected JSON payload:
        {
            "username": str,
            "email": str,
            "password": str
        }

    Returns:
        JSON response with user data or error message
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return jsonify({"error": "Missing required fields"}), 400

        # Validate input lengths
        if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
            return (
                jsonify({"error": "Username must be 5-25 characters"}),
                400,
            )

        if len(password) < MIN_PASSWORD_LENGTH:
            return (
                jsonify({"error": "Password must be at least 6 characters"}),
                400,
            )

        user = AuthService.register_user(username, email, password)

        if not user:
            return (
                jsonify({"error": "Username or email already exists"}),
                409,
            )

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": user.to_dict(),
                }
            ),
            201,
        )

    except Exception:
        logger.exception("Registration error")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/login", methods=["POST"])
def login() -> tuple[Any, int]:
    """Login user and create session.

    Expected JSON payload:
        {
            "username": str,
            "password": str
        }

    Returns:
        JSON response with user data or error message
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        password = data.get("password")

        if not all([username, password]):
            return jsonify({"error": "Missing required fields"}), 400

        user = AuthService.authenticate_user(username, password)

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # Create session
        session["user_id"] = user.id
        session["username"] = user.username

        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

    except Exception:
        logger.exception("Login error")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout() -> tuple[Any, int]:
    """Logout user and clear session.

    Returns:
        JSON response confirming logout
    """
    try:
        session.clear()
        return jsonify({"message": "Logout successful"}), 200
    except Exception:
        logger.exception("Logout error")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/me", methods=["GET"])
def get_current_user() -> tuple[Any, int]:
    """Get current logged-in user information.

    Returns:
        JSON response with user data or error if not authenticated
    """
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401

        user = AuthService.get_user_by_id(user_id)

        if not user:
            session.clear()
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user.to_dict()}), 200

    except Exception:
        logger.exception("Get current user error")
        return jsonify({"error": "Internal server error"}), 500
