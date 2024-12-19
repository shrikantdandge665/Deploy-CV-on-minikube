import unittest
from app import app

class ResumeAppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Shrikant Dandge", response.data)

    def test_invalid_route(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_css(self):
        with self.client.get('/static/style.css') as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"body", response.data)  # Optional: Check if CSS content is correct


    def test_performance(self):
        import time
        start_time = time.time()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.2)

if __name__ == '__main__':
    unittest.main()
