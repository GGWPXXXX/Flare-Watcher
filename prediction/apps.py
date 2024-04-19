from django.apps import AppConfig
import paho.mqtt.client as mqtt
from decouple import config
import threading
import json
from . import predict

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    
    def ready(self):
        self.mqtt_client = self.start_mqtt_client_thread()

    def start_mqtt_client_thread(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message
        
        mqtt_client.username_pw_set(config('MQTT_USER'), config('MQTT_PASS'))
        mqtt_client.connect(config('MQTT_BROKER'), config('MQTT_PORT', cast=int), 60)
        
        # start MQTT client in a separate thread
        mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()
        
        return mqtt_client

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe("b6510545608/year_project")
        else:
            print(f"Failed to connect to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
        predict.central_system(json.loads(msg.payload.decode()))
    
    def publish_mqtt_message(self, topic, message):
        self.mqtt_client.publish(topic, message)
