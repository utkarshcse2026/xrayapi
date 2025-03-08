# tests/test_api.py
import unittest
import os
import io
from app import create_app
import numpy as np
from PIL import Image

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_predict_no_file(self):
        response = self.client.post('/predict')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_predict_empty_file(self):
        response = self.client.post('/predict', data={
            'file': (io.BytesIO(), '')
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_predict_invalid_file_type(self):
        response = self.client.post('/predict', data={
            'file': (io.BytesIO(b'test data'), 'test.txt')
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_predict_valid_image(self):
        # Create a dummy grayscale image
        img_array = np.random.randint(0, 255, (224, 224), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        response = self.client.post('/predict', data={
            'file': (img_byte_arr, 'test.png')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', response.json)

if __name__ == '__main__':
    unittest.main()