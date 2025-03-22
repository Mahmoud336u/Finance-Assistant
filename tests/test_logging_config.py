import unittest
import logging
from logging_config import setup_logging

class TestLoggingConfig(unittest.TestCase):
    def test_setup_logging(self):
        # Test logging configuration
        setup_logging()
        logger = logging.getLogger('test')
        self.assertEqual(logger.level, logging.INFO)
        self.assertTrue(any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers))

if __name__ == "__main__":
    unittest.main()
