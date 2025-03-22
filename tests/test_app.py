import unittest
from unittest.mock import patch
from app import app
import json

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

    @patch('app.sagemaker')
    def test_get_recommendations(self, mock_sagemaker):
        # Mock SageMaker response
        mock_response = {'Body': json.dumps({'recommendation': 'save more'}).encode('utf-8')}
        mock_sagemaker.invoke_endpoint.return_value = mock_response
        response = self.app.get('/users/1/recommendations')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'recommendations': {'recommendation': 'save more'}})

if __name__ == "__main__":
    unittest.main()
