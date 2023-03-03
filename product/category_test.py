import unittest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from category_service import Category

Base = declarative_base()
class TestCategory(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_clone(self):
        # Test that cloning a Category returns an exact copy
        category1 = Category(name="Test Category")
        self.session.add(category1)
        self.session.commit()

        category2 = category1.clone()
        self.assertEqual(category1.id, category2.id)
        self.assertEqual(category1.name, category2.name)
        self.assertNotEqual(category1, category2)

if __name__ == '__main__':
    unittest.main()