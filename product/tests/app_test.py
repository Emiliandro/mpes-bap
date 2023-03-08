import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_by_id(self):
        response = self.app.post('/by_id', json={
            'message_id': 1})
        self.assertEqual(response.status_code, 200)

    def test_get_by_category(self):
        response = self.app.post('/by_category', json={
            'category': 'all'})
        self.assertEqual(response.status_code, 200)

    def test_get_between_date(self):
        response = self.app.post('/between_date', json={
            'from_date': '2022-01-01', 
            'until_date': '2024-01-02'})
        self.assertEqual(response.status_code, 200)

    def test_get_category_between_date(self):
        response = self.app.post('/category_between_date', json={
            'category': 'news', 
            'from_date': '2022-01-01', 
            'until_date': '2022-01-02'})
        self.assertEqual(response.status_code, 200)

    def test_add_message(self):
        response = self.app.post('/messages', json={
            'title': 'Test Title',
            'description': 'Test Description',
            'source': 'Test Source',
            'category': 'Test Category',
            'published_at': '2022-01-01T00:00:00Z'
        })
        self.assertEqual(response.status_code, 200)

    def test_update_message(self):
        response = self.app.put('/messages/1', json={
            'title': 'Updated Title',
            'description': 'Updated Description',
            'source': 'Updated Source',
            'category': 'Updated Category',
            'published_at': '2022-01-01T00:00:00Z'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_message(self):
        response = self.app.delete('/messages/1')
        self.assertEqual(response.status_code, 200)

    def test_add_category(self):
        response = self.app.post('/add_category', json={'category': 'Test Category'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
