import datetime
import os
from functools import wraps

import jwt
from flask import jsonify, request

# Fail fast if the secret is missing or too weak
_raw_secret = os.environ.get('JWT_SECRET_KEY', '')
if not _raw_secret:
    raise RuntimeError("JWT_SECRET_KEY environment variable must be set")
if len(_raw_secret) < 32:
    raise RuntimeError("JWT_SECRET_KEY must be at least 32 characters long")

SECRET_KEY: str = _raw_secret
TOKEN_EXPIRY_HOURS: int = int(os.getenv('JWT_EXPIRY_HOURS', '1'))


def token_required(f):
    """
    Decorator to require a valid JWT token for protected routes.

    Args:
        f (function): The route function to decorate.

    Returns:
        function: Decorated function with token validation.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Extract token from Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        try:
            # Decode and validate the token (expiry is enforced automatically)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']  # Extract user_id from token payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Pass the current_user to the route function
        return f(current_user, *args, **kwargs)
    return decorated


def generate_token(user_id: str) -> str:
    """
    Generate a JWT token with an expiry for a given user_id.

    Args:
        user_id (str): The user's identifier.

    Returns:
        str: Encoded JWT token.
    """
    now = datetime.datetime.utcnow()
    payload = {
        'user_id': user_id,
        'exp': now + datetime.timedelta(hours=TOKEN_EXPIRY_HOURS),
        'iat': now,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


if __name__ == "__main__":
    # Example usage for testing
    token = generate_token('user123')
    print(f"Generated Token: {token}")
