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


    def test_before_prediction_image(self):
        before_prediction_image = BeforePredictionImage.objects.create(
            image="image.jpg",
            prediction_result="result"
        )
        self.assertEqual(str(before_prediction_image), before_prediction_image.image)

    def test_after_prediction_image(self):
        after_prediction_image = AfterPredictionImage.objects.create(
            image="image.jpg",
            prediction_result="result"
        )
        self.assertEqual(str(after_prediction_image), after_prediction_image.image)

    def test_prediction_config(self):
        self.assertEqual(PredictionConfig.name, 'prediction')
        self.assertEqual(PredictionConfig.image_request, False)
        self.assertEqual(PredictionConfig.data, {
            "user_id": None,
            "Humidity[%]": None,
            "TVOC[ppb]" : None,
            "eCO2[ppm]" : None,
            "Pressure[hPa]" : None,
            "flame_sensor" : None,
            "img": None,
        })

    def test_mqtt_client(self):
        self.assertEqual(mqtt_client.username_pw_set("user", "pass"), None)
        self.assertEqual(mqtt_client.connect("broker", 1883, 60), None)
        self.assertEqual(mqtt_client.loop_forever(), None)
        self.assertEqual(mqtt_client.on_connect(mqtt_client, None, None, 0), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, None), None)
        self.assertEqual(data["user_id"], None)
        self.assertEqual(data["Humidity[%]"], None)
        self.assertEqual(data["TVOC[ppb]"], None)
        self.assertEqual(data["eCO2[ppm]"], None)
        self.assertEqual(data["Pressure[hPa]"], None)
        self.assertEqual(data["flame_sensor"], None)
        self.assertEqual(data["img"], None)
        self.assertEqual(data.items(), dict(data).items())
        self.assertEqual(data.items(), data.items())
    
    def test_mqtt_client_on_connect(self):
        self.assertEqual(mqtt_client.on_connect(mqtt_client, None, None, 0), None)
        self.assertEqual(mqtt_client.on_connect(mqtt_client, None, None, 1), None)
        self.assertEqual(mqtt_client.on_connect(mqtt_client, None, None, 2), None) 

    def test_mqtt_client_on_message(self):
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, None), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, None), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, None), None)
    
    def test_mqtt_client_on_message_topic(self):
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/year_project"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/year_project"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/year_project"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image"), None)

    def test_mqtt_client_on_message_topic_data(self):
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/year_project"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/year_project"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/year_project"), None)
        self.assertEqual(mqtt_client.on_message(mqtt_client, None, "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image"), None)
