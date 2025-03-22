import unittest
from unittest.mock import patch
from models import DeepSeekWrapper

class TestDeepSeekWrapper(unittest.TestCase):
    @patch('models.DeepSeekModel')
    def test_initialization(self, mock_model):
        # Test model wrapper initialization
        wrapper = DeepSeekWrapper()
        mock_model.assert_called_once()

    @patch('models.torch.load')
    @patch('models.DeepSeekModel')
    def test_load_model(self, mock_model, mock_load):
        # Test loading a model from a file
        mock_load.return_value = {'state': 'dummy'}
        wrapper = DeepSeekWrapper()
        wrapper.load_model('path/to/model.pth')
        mock_load.assert_called_once_with('path/to/model.pth')
        wrapper.model.load_state_dict.assert_called_once_with({'state': 'dummy'})
        wrapper.model.eval.assert_called_once()

    @patch('models.DeepSeekModel')
    def test_predict(self, mock_model):
        # Test prediction functionality
        mock_model.return_value = 'prediction'
        wrapper = DeepSeekWrapper()
        prediction = wrapper.predict('input text')
        self.assertEqual(prediction, 'prediction')

if __name__ == "__main__":
    unittest.main()
