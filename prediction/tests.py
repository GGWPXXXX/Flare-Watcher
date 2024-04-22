from django.test import TestCase, Client, RequestFactory, SimpleTestCase
from django.urls import reverse, resolve
from prediction.views import image_prediction_view, sensor_prediction_view
from prediction.apps import PredictionConfig
from prediction.models import BeforePredictionImage, AfterPredictionImage
from prediction.mqtt import mqtt_client, data
import json
import base64
from PIL import Image
import io

# Create your tests here.

class PredictionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_image_prediction_view(self):
        request = self.factory.post('/image_prediction/', data={"image": "data:image/jpeg;base64,base64data"})
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"serialized_result")

    def test_sensor_prediction_view(self):
        request = self.factory.post('/sensor_prediction/', data={"user_id": "test_user_id"})
        response = sensor_prediction_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"serialized_result")

    def test_image_prediction_view_get(self):
        request = self.factory.get('/image_prediction/')
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")

    def test_sensor_prediction_view_get(self):
        request = self.factory.get('/sensor_prediction/')
        response = sensor_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")
    
    def test_image_prediction_view_post(self):
        request = self.factory.post('/image_prediction/')
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")
    
    def test_sensor_prediction_view_post(self):
        request = self.factory.post('/sensor_prediction/')
        response = sensor_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")

    def test_image_prediction_view_image_data(self):
        request = self.factory.post('/image_prediction/', data={"image": "data:image/jpeg;base64,base64data"})
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"serialized_result")

    def test_image_prediction_view_image_data_png(self):
        request = self.factory.post('/image_prediction/', data={"image": "data:image/png;base64,base64data"})
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"serialized_result")

    def test_image_prediction_view_image_data_get(self):
        request = self.factory.get('/image_prediction/')
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")

    def test_image_prediction_view_image_data_post(self):
        request = self.factory.post('/image_prediction/')
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")

    def test_image_prediction_view_image_data_jpeg(self):
        request = self.factory.post('/image_prediction/', data={"image": "data:image/jpeg;base64,base64data"})
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"serialized_result")

    def test_image_prediction_view_image_data_png(self):
        request = self.factory.post('/image_prediction/', data={"image": "data:image/png;base64,base64data"})
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"serialized_result")

    def test_image_prediction_view_image_data_get(self):
        request = self.factory.get('/image_prediction/')
        response = image_prediction_view(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b"Method Not Allowed")

    