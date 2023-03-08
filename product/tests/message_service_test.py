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
        cls.engine = create_engine("sqlite:///:memory:")
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        Message.metadata.create_all(cls.engine)

    def setUp(self):
        self.service = MessageService()

    def tearDown(self):
        self.session.query(Message).delete()
        self.session.commit()

    def test_create_message(self):
        # Test creating a message with valid data
        title = "Test message"
        description = "This is a test message"
        source = "Test source"
        category = "Test category"
        date_string = "2022-01-01"
        self.service.create_message(title, description, source, category, date_string)
        messages = self.service.get_all_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["title"], title)

        # Test creating a message with an invalid date string
        title = "Test message 2"
        description = "This is another test message"
        source = "Test source"
        category = "Test category"
        date_string = "invalid date"
        response = self.service.create_message(title, description, source, category, date_string)
        self.assertEqual(response["error"], "Invalid datetime}")

    def test_get_message_by_id(self):
        # Test getting a message by ID
        title = "Test message"
        description = "This is a test message"
        source = "Test source"
        category = "Test category"
        date_string = "2022-01-01"
        message = self.service.create_message(title, description, source, category, date_string)
        message_id = message["id"]
        result = self.service.get_message_by_id(message_id)
        self.assertEqual(result["id"], message_id)
        self.assertEqual(result["title"], title)

        # Test getting a non-existent message by ID
        with self.assertRaises(ValueError):
            self.service.get_message_by_id(999)

    def test_get_messages_between_dates_with_category(self):
        self.service.create_message(
            title='Test Message 1',
            description='This is a test message',
            source='https://test.com',
            category='test',
            date_string='2022-03-01'
        )
        self.service.create_message(
            title='Test Message 2',
            description='This is another test message',
            source='https://test.com',
            category='test',
            date_string='2022-03-05'
        )

        messages = self.service.get_messages_between_dates_with_category(
            from_date=datetime(2022, 3, 1),
            to_date=datetime(2022, 3, 5),
            category='test'
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['title'], 'Test Message 1')
        self.assertEqual(messages[1]['title'], 'Test Message 2')

    def test_get_messages_between_dates_with_category_no_results(self):
        with self.assertRaises(ValueError):
            self.service.get_messages_between_dates_with_category(
                from_date=datetime(2022, 3, 1),
                to_date=datetime(2022, 3, 5),
                category='test'
            )

