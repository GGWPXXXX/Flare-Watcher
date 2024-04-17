from django.apps import AppConfig
import paho.mqtt.client as mqtt
from decouple import config


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    
    def ready(self):
        self.mqtt_client = start_mqtt_client()

    
def start_mqtt_client():
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    mqtt_client.username_pw_set(config('MQTT_USER'), config('MQTT_PASS'))
    mqtt_client.connect(config('MQTT_BROKER'), config('MQTT_PORT', cast=int), 60)
    mqtt_client.loop_start()
    
    return mqtt_client

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("b6510545608/year_project")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
