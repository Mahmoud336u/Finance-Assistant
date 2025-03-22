from flask import Flask, request, jsonify
import boto3
from sqlalchemy import create_engine
import os
import json

# Initialize Flask application
app = Flask(__name__)

# Database connection (e.g., Aurora Serverless)
engine = create_engine(os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/finance'))

# SageMaker runtime client for invoking ML endpoints
sagemaker = boto3.client('sagemaker-runtime')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Return the health status of the application."""
    return jsonify({'status': 'healthy'}), 200

# Fetch financial data for a user
@app.route('/users/<user_id>/financial_data', methods=['GET'])
def get_financial_data(user_id):
    """Retrieve financial data for a given user."""
    try:
        # Placeholder for fetching data from the database
        with engine.connect() as connection:
            # Example query (adjust based on your schema)
            result = connection.execute(f"SELECT * FROM financial_data WHERE user_id = '{user_id}'")
            data = [dict(row) for row in result.mappings()]
        return jsonify({'financial_data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get personalized recommendations for a user
@app.route('/users/<user_id>/recommendations', methods=['GET'])
def get_recommendations(user_id):
    """Generate personalized financial recommendations using SageMaker."""
    try:
        # Placeholder for fetching user features (e.g., from database or DynamoDB)
        features = {'user_id': user_id, 'income': 50000, 'expenses': 30000}  # Example data
        # Invoke SageMaker endpoint
        response = sagemaker.invoke_endpoint(
            EndpointName='recommendation-model',  # Replace with your endpoint name
            ContentType='application/json',
            Body=json.dumps(features)
        )
        result = json.loads(response['Body'].read().decode())
        return jsonify({'recommendations': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app (for development only; use Gunicorn in production)
    app.run(host='0.0.0.0', port=5000, debug=True)
