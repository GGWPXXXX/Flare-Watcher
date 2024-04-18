from django.apps import AppConfig
import paho.mqtt.client as mqtt
from decouple import config
import threading


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    
    def ready(self):
        self.mqtt_client = start_mqtt_client_thread()

def start_mqtt_client_thread():
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    mqtt_client.username_pw_set(config('MQTT_USER'), config('MQTT_PASS'))
    mqtt_client.connect(config('MQTT_BROKER'), config('MQTT_PORT', cast=int), 60)
    
    # Start MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
    mqtt_thread.daemon = True  # Daemonize thread
    mqtt_thread.start()
    
    return mqtt_client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("b6510545608/year_project")
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
