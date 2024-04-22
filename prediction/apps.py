from django.apps import AppConfig
import paho.mqtt.client as mqtt
from decouple import config
import threading
import json
from . import predict
from PIL import Image
import PIL
import io


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'

    image_request = False
    data = {
        "user_id": None,
        "Humidity[%]": None,
        "TVOC[ppb]" : None,
        "eCO2[ppm]" : None,
        "Pressure[hPa]" : None,
        "flame_sensor" : None,
        "img": None,
    }

    def ready(self):
        self.mqtt_client = self.start_mqtt_client_thread()

    def start_mqtt_client_thread(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message

        mqtt_client.username_pw_set(config('MQTT_USER'), config('MQTT_PASS'))
        mqtt_client.connect(config('MQTT_BROKER'),
                            config('MQTT_PORT', cast=int), 60)

        # start MQTT client in a separate thread
        mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()

        return mqtt_client

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe("b6510545608/year_project")
            client.subscribe(
                "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image")
        else:
            print(f"Failed to connect to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message on topic '{msg.topic}'")
        # if receive sensor data
        if msg.topic == "b6510545608/year_project":
            # extract sensor data from message
            recv_data = json.loads(msg.payload.decode())
            self.data["user_id"] = recv_data["user_id"]
            self.data["Humidity[%]"] = recv_data["Humidity[%]"]
            self.data["TVOC[ppb]"] = recv_data["TVOC[ppb]"]
            self.data["eCO2[ppm]"] = recv_data["eCO2[ppm]"]
            self.data["Pressure[hPa]"] = recv_data["Pressure[hPa]"]
            self.data["flame_sensor"] = recv_data["flame_sensor"]
            print(self.data.items())
            # send request to get image
            self.publish_mqtt_message(
                "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/shutter", 1)
            self.image_request = True
        elif msg.topic == "b6510545608/camera/462de33d-2624-486b-b1b7-5a534a23a267/image":
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
                    predict.central_system(self.data)
                except PIL.UnidentifiedImageError as e:
                    print(f"Error opening image: {e}")
                # predict.image_prediction(image_data)

    def publish_mqtt_message(self, topic, message):
        self.mqtt_client.publish(topic, message)
