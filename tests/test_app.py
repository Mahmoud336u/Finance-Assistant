import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'healthy'})

    def test_get_financial_data(self):
        response = self.app.get('/users/1/financial_data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('financial_data', response.json)

if __name__ == "__main__":
    unittest.main()
