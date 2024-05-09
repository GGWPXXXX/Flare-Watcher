from django.apps import AppConfig
import paho.mqtt.client as mqtt
from decouple import config
import threading
import json
from . import predict
from PIL import Image
import PIL
import io

MQTT_SENSOR_TOPIC = config("MQTT_SENSOR_TOPIC")


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    app_module = 'prediction.apps'
    path = 'prediction/apps.py'

    uuid = None
    user_id = None
    image_request = False
    data = {
        "user_id": None,
        "Humidity[%]": None,
        "TVOC[ppb]": None,
        "eCO2[ppm]": None,
        "Pressure[hPa]": None,
        "img": None,
        "flame_sensor": None
    }

    def ready(self):
        """ Start the MQTT client when the app is ready """
        self.mqtt_client = self.start_mqtt_client_thread()

    def start_mqtt_client_thread(self):
        """ Start an MQTT client that connects to the broker and subscribes to the sensor topic """
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message

        mqtt_client.username_pw_set(config('MQTT_USER'), config('MQTT_PASS'))
        mqtt_client.connect(config('MQTT_BROKER'),
                            config('MQTT_PORT', cast=int), 60)

        # Start MQTT client in a separate thread
        mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()

        return mqtt_client

    def on_connect(self, client, userdata, flags, rc):
        """ Callback function that is called when the MQTT client connects to the broker"""
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe(MQTT_SENSOR_TOPIC)
            client.subscribe(f"b6510545608/camera/+/image")
        else:
            print(f"Failed to connect to MQTT broker with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        """ Callback function that is called when the MQTT client disconnects from the broker """
        print(f"Disconnected from MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        """ Callback function that is called when a message is received on a subscribed topic """
        print(f"Received message on topic '{msg.topic}'")
        # if receive sensor data
        if msg.topic == MQTT_SENSOR_TOPIC:
            # extract sensor data from message
            recv_data = json.loads(msg.payload.decode())
            self.uuid = recv_data["uuid"]
            self.user_id = recv_data["user_id"]
            self.data["user_id"] = recv_data["user_id"]
            self.data["Humidity[%]"] = recv_data["Humidity[%]"]
            self.data["TVOC[ppb]"] = recv_data["TVOC[ppb]"]
            self.data["eCO2[ppm]"] = recv_data["eCO2[ppm]"]
            self.data["Pressure[hPa]"] = recv_data["Pressure[hPa]"]
            self.data["flame_sensor"] = recv_data["flame_sensor"]
            self.data["is_live_data"] = recv_data["is_live_data"]
            print(self.data.items())
            # send request to get image
            self.publish_mqtt_message(
                f"b6510545608/camera/{self.uuid}/shutter", 1)
            print(f"b6510545608/camera/{self.uuid}/shutter")
            self.image_request = True
        elif msg.topic == f"b6510545608/camera/{self.uuid}/image":
            if self.image_request:
                print("Image received")
                self.image_request = False
                # Print length and first few bytes of the received payload
                print(f"Payload length: {len(msg.payload)}")
                print(f"Payload start: {msg.payload[:10]}")
                try:
                    image = Image.open(io.BytesIO(msg.payload))
                    self.data["img"] = image
                    print(self.data.items())

                    # dump both image and sensor data into processing unit
                    predict.central_system(self.data)
                except PIL.UnidentifiedImageError as e:
                    print(f"Error opening image: {e}")
                # predict.image_prediction(image_data)

    def publish_mqtt_message(self, topic, message):
        """ Publish a message to the MQTT broker """
        self.mqtt_client.publish(topic, message)
