from machine import Pin, I2C, ADC
import network
import uasyncio as asyncio
from umqtt.robust import MQTTClient
from bme280 import BME280, BME280_OSAMPLE_2, BME280_I2CADDR
from sht3x import SHT3x
from sgp30 import Adafruit_SGP30 
import json
from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS

# MQTT Broker details

USER_ID = ""

UUID = ""

MQTT_BROKER_NAKE = ''
MQTT_USER_NAKE = ''
MQTT_PASS_NAKE = ''


# LED setup for visual feedback
led = Pin(12, Pin.OUT)

# Set up the I2C bus and sensors

i2c = I2C(1, sda=Pin(4), scl=Pin(5))

flame_sensor = Pin(33, Pin.IN)

bme280 = BME280(mode=BME280_OSAMPLE_2, address=BME280_I2CADDR, i2c=i2c)
sht30 = SHT3x(i2c)
sgp30 = Adafruit_SGP30(i2c)

# Initialize the network interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Function to handle WiFi connection
def connect_to_wifi():
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            print("Trying to connect...")
            asyncio.sleep(0.5)
    print("Connected to WiFi!")

# Connect to WiFi on startup
connect_to_wifi()

# MQTT Client setup
mqtt = MQTTClient(client_id="", server=MQTT_BROKER_NAKE, user=MQTT_USER_NAKE, password=MQTT_PASS_NAKE)
mqtt.connect()
print("Connected to MQTT Broker!")

def sub_callback(topic, payload):
    if topic.decode() == f"b6510545608/request_live_data/{USER_ID}":
        print("Here")
        publisher()

# LED blinking function for indication
def blink_led():
    for _ in range(5): 
        led.value(1)
        asyncio.sleep(0.2)
        led.value(0)
        asyncio.sleep(0.2)

# Publisher coroutine
async def publisher():
#     while True:
    if not wlan.isconnected():
        connect_to_wifi()  # Ensure connection is up
    try:
        # Read data from sensors
        
        bme_temp, bme_pressure, bme_humidity = bme280.read_compensated_data()
        bme_temp = bme_temp / 100.0
        bme_pressure = bme_pressure / 25600.0
        bme_humidity = bme_humidity / 1024.0
        
        sht30.measure()
        sht_humidity, sht_temp = sht30.ht()
        
        temp = (bme_temp + sht_temp) / 2
        pressure = bme_pressure
        humidity = (bme_humidity + sht_humidity) / 2
        
        co2eq, tvoc = sgp30.iaq_measure()
        
        flame_detected = flame_sensor.value()
        
        data = {
            'user_id' : USER_ID,
            'uuid' : UUID,
            'Humidity[%]': humidity,
            'TVOC[ppb]': tvoc,
            'eCO2[ppm]': co2eq,
            'Pressure[hPa]': pressure,
            'flame_sensor' : flame_detected
        }
        
        # Publish data to MQTT Broker
        mqtt.publish(f'{MQTT_USER_NAKE}/sensor_data', json.dumps(data))
#             print("Data published!")
#             await asyncio.sleep(600)
    except Exception as e:
        print("An error occurred:", e)
        blink_led()

# Check message sending coroutine
async def send_check():
    count = 0
    while True:
        try:
            mqtt.publish(f'{MQTT_USER_NAKE}/check', f"Count: {count}")
            print(f'Count: {count}')
            await asyncio.sleep(60)
            count += 1
        except Exception as e:
            print("Error sending check message:", e)
            blink_led()

# Setup asyncio loop

mqtt.subscribe(f"b6510545608/request_live_data/{USER_ID}")

loop = asyncio.get_event_loop()
loop.create_task(publisher())
loop.create_task(send_check())
loop.run_forever()



