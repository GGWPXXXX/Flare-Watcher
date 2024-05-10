from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS, USER_ID, UUID
from time import sleep
import network
import json
import _thread
from umqtt.robust import MQTTClient
import json
from bme280 import BME280, BME280_OSAMPLE_2, BME280_I2CADDR
from sht3x import SHT3x
from sgp30 import Adafruit_SGP30
from machine import Pin, I2C



i2c = I2C(1, sda=Pin(4), scl=Pin(5))
flame_sensor = Pin(18, Pin.IN)
bme280 = BME280(mode=BME280_OSAMPLE_2, address=BME280_I2CADDR, i2c=i2c)
sht30 = SHT3x(i2c)
sgp30 = Adafruit_SGP30(i2c)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if wlan.isconnected() == False:
    wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    print("Can't connect :(")
    sleep(0.5)
print("Connected!")


mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

def sub_callback(topic, payload):
    print(topic.decode())
    if topic.decode() == f"public/request_live_data/{USER_ID}":
        print("Here")
        bme_temp, bme_pressure, bme_humidity = bme280.read_compensated_data()
        sht30.measure()
        sht_humidity, sht_temp = sht30.ht()
        co2eq, tvoc = sgp30.iaq_measure()
        flame_detected = flame_sensor.value()
        
        data = {
        "user_id": USER_ID,
        "uuid":UUID ,
        "Humidity[%]": (bme_humidity / 1024.0 + sht_humidity) / 2,
        "TVOC[ppb]": tvoc,
        "eCO2[ppm]": co2eq,
        "Pressure[hPa]": bme_pressure / 25600.0,
        "flame_sensor": flame_detected,
        "is_live_data": 1
        }
        mqtt.publish("public/flarewatcher/sensor_data", json.dumps(data))
        print("Request sent!")


def send_data_every_10sec():
    timer = 1
    while True:
        print(timer)
        if timer % 10 == 0:
            bme_temp, bme_pressure, bme_humidity = bme280.read_compensated_data()
            sht30.measure()
            sht_humidity, sht_temp = sht30.ht()
            co2eq, tvoc = sgp30.iaq_measure()
            flame_detected = flame_sensor.value()
            
            data = {
            "user_id": USER_ID,
            "uuid":UUID ,
            "Humidity[%]": (bme_humidity / 1024.0 + sht_humidity) / 2,
            "TVOC[ppb]": tvoc,
            "eCO2[ppm]": co2eq,
            "Pressure[hPa]": bme_pressure / 25600.0,
            "flame_sensor": flame_detected,
            "is_live_data": 0
                }
            mqtt.publish("public/flarewatcher/sensor_data", json.dumps(data))
            print("10 Seconds Sent!")
        sleep(1)
        timer += 1
      

mqtt.connect()
mqtt.set_callback(sub_callback)
mqtt.subscribe(f"b6510545608/request_live_data/{USER_ID}")
_thread.start_new_thread(send_data_every_10sec, ())
while True:
    mqtt.check_msg()
    sleep(0.5)