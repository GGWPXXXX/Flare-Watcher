import PIL
import json
import base64
import io
import numpy as np
from PIL import Image
from django.test import TestCase, Client, RequestFactory, SimpleTestCase
from django.urls import reverse, resolve
from prediction.models import BeforePredictionImage, OriginalSizePredictionImage, CompressedPredictionImage
from prediction import predict

from django.test import TestCase
from unittest.mock import patch, MagicMock, call
from prediction.apps import PredictionConfig, MQTT_SENSOR_TOPIC
from ultralytics import YOLO


class PredictionConfigTestCase(TestCase):

    def setUp(self):
        # Properly setting up a PredictionConfig instance with necessary parameters
        self.app_config = PredictionConfig('prediction', 'prediction.apps')
        self.mqtt_client_mock = MagicMock()
        self.app_config.mqtt_client = self.mqtt_client_mock

    @patch('paho.mqtt.client.Client')
    def test_mqtt_client_thread_starts(self, mqtt_client_mock):
        # Ensure that the MQTT client starts correctly
        mqtt_instance = mqtt_client_mock.return_value
        self.app_config.start_mqtt_client_thread()
        mqtt_instance.loop_forever.assert_called_once()

    def test_on_connect_success(self):
        # Simulate successful connection
        client1 = self.mqtt_client_mock
        client2 = self.mqtt_client_mock
        self.app_config.on_connect(client1, None, None, 0)
        self.app_config.on_connect(client2, None, None, 0)
        
        # Check that subscribe was called with both topics
        expected_calls = [call('b6510545608/camera/+/image'), call('public/flarewatcher/sensor_data')]
        self.mqtt_client_mock.subscribe.assert_has_calls(expected_calls, any_order=True)


    def test_on_connect_failure(self):
        # Simulate failed connection
        self.app_config.on_connect(self.mqtt_client_mock, None, None, 1)
        self.mqtt_client_mock.subscribe.assert_not_called()
        
    @patch('json.loads')
    @patch('prediction.apps.PredictionConfig.publish_mqtt_message')
    def test_on_message_sensor_data(self, publish_mock, json_loads_mock):
        # Setup mock to simulate received sensor data
        json_loads_mock.return_value = {
            "uuid": "unique-id",
            "user_id": "user123",
            "Humidity[%]": 45,
            "TVOC[ppb]": 150,
            "eCO2[ppm]": 600,
            "Pressure[hPa]": 1010,
            "flame_sensor": False,
            "is_live_data": True
        }
        message_mock = MagicMock()
        message_mock.payload.decode.return_value = json.dumps(json_loads_mock.return_value)
        message_mock.topic = MQTT_SENSOR_TOPIC

        # Call on_message with mocked data
        self.app_config.on_message(self.mqtt_client_mock, None, message_mock)

        # Verify data extraction and processing
        self.assertEqual(self.app_config.data["Humidity[%]"], 45)
        self.assertEqual(self.app_config.data["user_id"], "user123")
        publish_mock.assert_called_with(f"b6510545608/camera/{self.app_config.uuid}/shutter", 1)

    def test_on_disconnect(self):
        # Simulate disconnection
        self.app_config.on_disconnect(self.mqtt_client_mock, None, 0)

        # Check for proper logging or any other disconnection handling
        # This will require that you check for the output or side-effects as per your application's logic
        print("Disconnected from MQTT broker with result code 0")  # This is a placeholder for actual verification

    def test_on_message_image_reception_failure(self):
        # Simulate receiving a corrupted image
        message_mock = MagicMock()
        message_mock.payload = b'corrupted data'
        message_mock.topic = f"b6510545608/camera/{self.app_config.uuid}/image"
        self.app_config.image_request = True  # Set flag as if waiting for image

        # Call on_message and simulate image opening failure
        with patch('PIL.Image.open', side_effect=PIL.UnidentifiedImageError("Cannot identify image file")):
            self.app_config.on_message(self.mqtt_client_mock, None, message_mock)

        # Assert that image_request flag is reset and no further processing is triggered
        self.assertFalse(self.app_config.image_request)
        self.assertIsNone(self.app_config.data["img"])

    @patch('prediction.apps.predict.central_system')
    def test_on_message_image_reception_success(self, central_system_mock):
        # Simulate receiving a valid image
        message_mock = MagicMock()
        message_mock.payload = b'valid image data'
        message_mock.topic = f"b6510545608/camera/{self.app_config.uuid}/image"
        self.app_config.image_request = True

        # Call on_message and simulate image opening success
        with patch('PIL.Image.open', return_value=MagicMock()):
            self.app_config.on_message(self.mqtt_client_mock, None, message_mock)

        # Assert that image_request flag is reset and further processing is triggered
        self.assertFalse(self.app_config.image_request)
        central_system_mock.assert_called_once()

    @patch('prediction.apps.PredictionConfig.publish_mqtt_message')

    def test_publish_mqtt_message(self, publish_mock):
        # Ensure that the message is published correctly
        topic = "test/topic"
        message = "test message"
        self.app_config.publish_mqtt_message(topic, message)
        publish_mock.assert_called_with(topic, message)


# from . import predict
# from prediction.apps import PredictionConfig
# from unittest.mock import patch, MagicMock, call
# from prediction.apps import PredictionConfig, MQTT_SENSOR_TOPIC
# from ultralytics import YOLO
# from PIL import Image
# from prediction.predict import sensor_prediction, central_system
# import io
# import json

# class PredictTestCase(TestCase):

#     @patch('prediction.predict.load_random_forest_model')
#     def test_sensor_prediction(self, load_mock):
#         model_mock = MagicMock()
#         load_mock.return_value = model_mock
#         model_mock.predict.return_value = [1]  # Mock the predict to return a list

#         sensor_prediction([1, 2, 3, 4])

#         # Get the actual arguments passed to the predict call
#         args, kwargs = model_mock.predict.call_args

#         # Use numpy.array_equal to check if arrays are equal
#         expected = np.array([[1, 2, 3, 4]])
#         actual = args[0]
#         self.assertTrue(np.array_equal(actual, expected), "Arrays do not match.")




#     @patch('pickle.load')
#     @patch('builtins.open')
#     def test_load_random_forest_model(self, open_mock, pickle_load_mock):
#         # Ensure that the random forest model is loaded correctly
#         predict.load_random_forest_model()
#         open_mock.assert_called_with('prediction/model/random_forest_model.pkl', 'rb')
#         pickle_load_mock.assert_called_once()

#     @patch('prediction.predict.load_random_forest_model')
#     def test_sensor_prediction(self, load_mock):
#         model_mock = MagicMock()
#         load_mock.return_value = model_mock
#         model_mock.predict.return_value = [1]  # Mock predict to return a list

#         predict.sensor_prediction([1, 2, 3, 4])

#         # Instead of directly comparing DataFrames, check call args separately
#         args, kwargs = model_mock.predict.call_args
#         self.assertTrue((args[0] == np.array([[1, 2, 3, 4]])).all())


#     @patch('prediction.predict.image_prediction')
#     @patch('prediction.predict.sensor_prediction')
#     def test_on_message_sensor_data(self, sensor_mock, image_prediction_mock):
#         image_prediction_mock.return_value = None  # Assuming the function doesn't need to return anything specific for this test
#         data = {
#             "Humidity[%]": 45, "TVOC[ppb]": 150, "eCO2[ppm]": 600, "Pressure[hPa]": 1010,
#             "flame_sensor": False, "is_live_data": True, "img": MagicMock()  # Mock image
#         }
        
#         central_system(data)  # Call this to potentially trigger sensor_prediction

#         # Check if sensor_mock was called with the expected arguments
#         expected_call_args = [45, 150, 600, 1010]
#         sensor_mock.assert_called_once_with(expected_call_args)




 