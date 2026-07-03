import io
import json
import os
import unittest
from unittest.mock import patch

# Set required environment variables before importing the app module
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')
os.environ.setdefault('JWT_SECRET_KEY', 'test-secret-key-that-is-long-enough-32chars')

from app import app  # noqa: E402


class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        # Test the /health endpoint
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'healthy'})

    @patch('app.engine')
    def test_get_financial_data(self, mock_engine):
        # Mock database engine response
        mock_result = [{'id': 1, 'user_id': '1', 'amount': 100.0}]
        mock_engine.connect.return_value.__enter__.return_value.execute.return_value.mappings.return_value = mock_result
        response = self.app.get('/users/1/financial_data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'financial_data': mock_result})

    def test_get_financial_data_invalid_user_id(self):
        # SQL-injection-style or otherwise invalid user_id must be rejected
        response = self.app.get("/users/' OR '1'='1'/financial_data")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    @patch('app._get_sagemaker_client')
    def test_get_recommendations(self, mock_get_client):
        # Mock SageMaker response – Body must expose a .read() method
        body_bytes = json.dumps({'recommendation': 'save more'}).encode('utf-8')
        mock_get_client.return_value.invoke_endpoint.return_value = {'Body': io.BytesIO(body_bytes)}
        response = self.app.get('/users/1/recommendations')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'recommendations': {'recommendation': 'save more'}})

    def test_get_recommendations_invalid_user_id(self):
        # user_id longer than 50 characters must be rejected before calling SageMaker
        long_user_id = 'a' * 51
        response = self.app.get(f'/users/{long_user_id}/recommendations')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)


if __name__ == "__main__":
    unittest.main()
