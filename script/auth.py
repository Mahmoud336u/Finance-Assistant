from flask import request, jsonify
from functools import wraps
import jwt
import os

# Secret key for JWT (in production, store this in AWS Secrets Manager or environment variables)
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

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
            # Decode and validate the token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']  # Extract user_id from token payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        # Pass the current_user to the route function
        return f(current_user, *args, **kwargs)
    return decorated

# Example helper function to generate a token (for testing purposes)
def generate_token(user_id):
    """
    Generate a JWT token for a given user_id.
    
    Args:
        user_id (str): The user's identifier.
    
    Returns:
        str: Encoded JWT token.
    """
    payload = {'user_id': user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

if __name__ == "__main__":
    # Example usage for testing
    token = generate_token('user123')
    print(f"Generated Token: {token}")
