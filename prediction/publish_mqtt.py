from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS
from time import sleep
import upip
import network
import json
from umqtt.robust import MQTTClient
import usocket

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if wlan.isconnected() == False:
    wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    print("Can't connect :(")
    sleep(0.5)
print("Connected!")

try:
    import urequests
except ImportError:
    print("Installing urequests ...")
    upip.install('urequests')
    print("Done!")

mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

def sub_callback(topic, payload):
    pass

mqtt.connect()
mqtt.set_callback(sub_callback)
mqtt.subscribe("b6510545608/year_project")

while True:
    data = {
      "user_id":'1235467890',
      "Humidity[%]": 50.61,
      "TVOC[ppb]": 741,
      "eCO2[ppm]": 600,
      "Pressure[hPa]": 0
    }
    mqtt.publish('b6510545608/year_project', json.dumps(data))
    print(f"Sent data!")
    sleep(100)



