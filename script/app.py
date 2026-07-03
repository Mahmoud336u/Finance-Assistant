import json
import logging
import os
import re

import boto3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import create_engine, text

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# CORS – allowed origins configured via environment variable (comma-separated)
_allowed_origins = [o.strip() for o in os.getenv('ALLOWED_ORIGINS', '').split(',') if o.strip()]
CORS(app, origins=_allowed_origins)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Database connection – DATABASE_URL must be set in the environment
_database_url = os.environ.get('DATABASE_URL')
if not _database_url:
    raise RuntimeError("DATABASE_URL environment variable is required")
engine = create_engine(_database_url)

# SageMaker runtime client – lazily initialized to avoid region errors at import time
_sagemaker_endpoint = os.environ.get('SAGEMAKER_ENDPOINT', 'recommendation-model')
_sagemaker_client = None


def _get_sagemaker_client():
    global _sagemaker_client
    if _sagemaker_client is None:
        _sagemaker_client = boto3.client('sagemaker-runtime')
    return _sagemaker_client


def _validate_user_id(user_id: str) -> bool:
    """Return True only for non-empty alphanumeric IDs up to 50 characters."""
    return bool(user_id) and bool(re.match(r'^[a-zA-Z0-9_-]{1,50}$', user_id))


@app.after_request
def set_security_headers(response):
    """Attach standard security headers to every response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Return the health status of the application."""
    return jsonify({'status': 'healthy'}), 200


# Fetch financial data for a user
@app.route('/users/<user_id>/financial_data', methods=['GET'])
@limiter.limit("30 per minute")
def get_financial_data(user_id):
    """Retrieve financial data for a given user."""
    if not _validate_user_id(user_id):
        return jsonify({'error': 'Invalid user_id'}), 400

    try:
        with engine.connect() as connection:
            # Parameterized query prevents SQL injection
            result = connection.execute(
                text("SELECT * FROM financial_data WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            data = [dict(row) for row in result.mappings()]
        return jsonify({'financial_data': data}), 200
    except Exception:
        logger.exception("Error fetching financial data for user %s", user_id)
        return jsonify({'error': 'An internal error occurred'}), 500


# Get personalized recommendations for a user
@app.route('/users/<user_id>/recommendations', methods=['GET'])
@limiter.limit("30 per minute")
def get_recommendations(user_id):
    """Generate personalized financial recommendations using SageMaker."""
    if not _validate_user_id(user_id):
        return jsonify({'error': 'Invalid user_id'}), 400

    try:
        features = {'user_id': user_id, 'income': 50000, 'expenses': 30000}
        response = _get_sagemaker_client().invoke_endpoint(
            EndpointName=_sagemaker_endpoint,
            ContentType='application/json',
            Body=json.dumps(features),
        )
        result = json.loads(response['Body'].read().decode())
        return jsonify({'recommendations': result}), 200
    except Exception:
        logger.exception("Error fetching recommendations for user %s", user_id)
        return jsonify({'error': 'An internal error occurred'}), 500


if __name__ == "__main__":
    # Use FLASK_DEBUG=1 to enable debug mode (development only)
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
