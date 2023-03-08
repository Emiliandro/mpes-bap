from urllib.error import URLError, HTTPError
from unittest.mock import MagicMock, patch

import unittest

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# now you can import module1 from the parent directory
from data_helper import DataHelper


class TestDataHelper(unittest.TestCase):

    def setUp(self):
        self.helper = DataHelper()

    def test_removeNotPortuguese(self):
        messages = [
            {"description": "This is a test message", "source": "source1"},
            {"description": "Esta é uma mensagem de teste", "source": "source2"},
            {"description": "This is another test message", "source": "source3"},
            {"description": "Esta é outra mensagem de teste", "source": "source1"},
        ]
        expected = [
            {"description": "Esta é uma mensagem de teste", "source": "source2"},
            {"description": "Esta é outra mensagem de teste", "source": "source1"},
        ]

        filtered = self.helper.removeNotPortuguese(messages)
        self.assertEqual(filtered, expected)

    def test_removeMinDescription(self):
        # Arrange
        messages = [
            {"description": "1234567890", "source": "source1"},
            {"description": "", "source": "source2"},
            {"source": "source3"},
            {"description": "123456789012345678901234567890", "source": "source1"},
            {"description": "123456789012345678901234567890123456789012345678901234567890", "source": "source1"}
        ]
        data_helper = DataHelper()

        # Act
        filtered = data_helper.removeMinDescription(messages)

        # Assert
        expected = [{"description": "123456789012345678901234567890123456789012345678901234567890", "source": "source1"}]
        self.assertEqual(filtered, expected)


    def test_removeDuplicates(self):
        messages = [{"description": "This is a test message", "source": "source1"},
            {"description": "This is another test message", "source": "source3"},
            {"description": "This is a test message", "source": "source2"},
            {"description": "Esta é outra mensagem de teste", "source": "source1"},
            {"description": "This is a test message", "source": "source2"}]

        expected = [{"description": "This is a test message", "source": "source1"},
            {"description": "This is another test message", "source": "source3"},
            {'description': 'This is a test message', 'source': 'source2'}]

        helper = DataHelper()
        filtered = helper.removeDuplicates(messages)

        self.assertEqual(filtered, expected)


    def test_validateUrl(self):
        with patch("data_helper.urlopen", return_value=MagicMock()):
            self.assertTrue(self.helper.validateUrl("http://www.google.com"))
        
        with patch("data_helper.urlopen", side_effect=HTTPError("", 404, "", None, None)):
            self.assertFalse(self.helper.validateUrl("http://www.google.com/notfound"))

        with patch("data_helper.urlopen", side_effect=URLError("Connection refused")):
            self.assertFalse(self.helper.validateUrl("http://localhost:9999"))

if __name__ == '__main__':
    unittest.main()
