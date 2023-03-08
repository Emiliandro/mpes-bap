import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# now you can import module1 from the parent directory
from message_service import Message, MessageService

class TestMessageService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = MessageService()
        cls.test_messages = [
            {"title": "Test Message 1", "description": "This is a test message.", "source": "Test Source 1", "category": "Test Category 1", "published_at": "2023-03-01"},
            {"title": "Test Message 2", "description": "This is another test message.", "source": "Test Source 2", "category": "Test Category 2", "published_at": "2023-03-02"},
            {"title": "Test Message 3", "description": "This is yet another test message.", "source": "Test Source 3", "category": "Test Category 1", "published_at": "2023-03-03"}
        ]
        cls.service.create_messages(cls.test_messages)

    @classmethod
    def tearDownClass(cls):
        cls.service.session.query(Message).delete()
        cls.service.session.commit()

    def test_get_all_messages(self):
        messages = self.service.get_all_messages()
        self.assertEqual(len(messages), 3)

    def test_get_message_by_category(self):
        messages = self.service.get_message_by_category("Test Category 1")
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["title"], "Test Message 1")
        self.assertEqual(messages[1]["title"], "Test Message 3")

    def test_get_message_by_id(self):
        message_id = self.service.session.query(Message.id).filter(Message.title=="Test Message 1").first()[0]
        message = self.service.get_message_by_id(message_id)
        self.assertEqual(message["title"], "Test Message 1")

    def test_get_message_between_dates(self):
        from_date = datetime(2023, 3, 2)
        to_date = datetime(2023, 3, 3)
        messages = self.service.get_message_between_dates(from_date, to_date)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["title"], "Test Message 2")
        self.assertEqual(messages[1]["title"], "Test Message 3")

    def test_get_messages_between_dates_with_category(self):
        from_date = datetime(2023, 3, 2)
        to_date = datetime(2023, 3, 3)
        messages = self.service.get_messages_between_dates_with_category(from_date, to_date, "Test Category 1")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["title"], "Test Message 3")

    def test_create_message(self):
        title = "New Test Message"
        description = "This is a new test message."
        source = "New Test Source"
        category = "New Test Category"
        date_string = "2023-03-04"
        message = self.service.create_message(title, description, source, category, date_string)
        self.assertEqual(message["title"], title)
        self.assertEqual(message["description"], description)
        self.assertEqual(message["source"], source)
        self.assertEqual(message["category"], category)
        self.assertEqual(message["published_at"], date_string)

if __name__ == '__main__':
    unittest.main()
