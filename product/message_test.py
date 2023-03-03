import unittest
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from message_service import Message

Base = declarative_base()

class TestMessage(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_published_at(self):
        # Test that published_at defaults to the current time
        message = Message(title="Test Message", description="This is a test message", source="Test Source", category="Test Category")
        self.session.add(message)
        self.session.commit()
        self.assertTrue(isinstance(message.published_at, datetime))

if __name__ == '__main__':
    unittest.main()
