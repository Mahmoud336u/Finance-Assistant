import unittest
from unittest.mock import patch
from config import config

class TestConfig(unittest.TestCase):
    def test_development_config(self):
        # Test development environment config
        dev_config = config['development']
        self.assertTrue(dev_config.DEBUG)
        self.assertEqual(dev_config.DATABASE_URL, 'sqlite:///dev.db')  # Default if not set

    @patch.dict('os.environ', {}, clear=True)
    def test_production_config(self):
        # Test production environment config without any DATABASE_URL in env
        from importlib import reload
        import config as config_module
        reload(config_module)
        prod_config = config_module.config['production']
        self.assertFalse(prod_config.DEBUG)
        self.assertIsNone(prod_config.DATABASE_URL)  # None if not set in environment

    def test_testing_config(self):
        # Test testing environment config
        test_config = config['testing']
        self.assertTrue(test_config.TESTING)
        self.assertEqual(test_config.DATABASE_URL, 'sqlite:///:memory:')

if __name__ == "__main__":
    unittest.main()
