"""Authentication service for user management."""

from __future__ import annotations

import logging

from backend.database import db
from backend.models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """Service for user authentication and management."""

    @staticmethod
    def register_user(username: str, email: str, password: str) -> User | None:
        """Register a new user.

        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)

        Returns:
            User: Created user object or None if registration fails
        """
        try:
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                logger.warning("Username already exists: %s", username)
                return None

            if User.query.filter_by(email=email).first():
                logger.warning("Email already exists: %s", email)
                return None

            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            logger.info("New user registered: %s", username)
        except Exception:
            db.session.rollback()
            logger.exception("Error registering user")
            return None
        else:
            return user

    @staticmethod
    def authenticate_user(username: str, password: str) -> User | None:
        """Authenticate a user with username and password.

        Args:
            username: Username
            password: Plain text password

        Returns:
            User: User object if authentication successful, None otherwise
        """
        try:
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                user.update_last_login()
                db.session.commit()
                logger.info("User authenticated: %s", username)
            else:
                logger.warning("Authentication failed for user: %s", username)
                return None
        except Exception:
            logger.exception("Error authenticating user")
            return None
        else:
            return user

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User: User object or None if not found
        """
        try:
            return db.session.get(User, user_id)
        except Exception:
            logger.exception("Error fetching user by ID")
            return None

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        """Get user by username.

        Args:
            username: Username

        Returns:
            User: User object or None if not found
        """
        try:
            return User.query.filter_by(username=username).first()
        except Exception:
            logger.exception("Error fetching user by username")
            return None
