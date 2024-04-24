import network
import urequests
from machine import I2C, Pin
from time import sleep
from lib.bme280 import BME280, BME280_OSAMPLE_2, BME280_I2CADDR
from lib.sht3x import SHT3x
from config import WIFI_SSID, WIFI_PASS

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            print("Trying to connect...")
            sleep(0.5)
    print("Connected to WiFi!")
    return wlan

wlan = connect_to_wifi()

# Setup I2C
i2c = I2C(1, sda=Pin(4), scl=Pin(5))
bme280 = BME280(mode=BME280_OSAMPLE_2, address=BME280_I2CADDR, i2c=i2c)
sht30 = SHT3x(i2c)

# Endpoint URL
url = 'https://flare-watcher-production.up.railway.app/predict/sensor_prediction/'

# Send data loop
while True:
    if not wlan.isconnected():
        wlan = connect_to_wifi()  # Reconnect if connection is lost

    # Get data from BME280
    bme_temp, bme_pressure, bme_humidity = bme280.read_compensated_data()
    bme_temp = bme_temp / 100.0
    bme_pressure = bme_pressure / 25600.0
    bme_humidity = bme_humidity / 1024.0

    try:
        sht30.measure()
        sht_humidity, sht_temp = sht30.ht()
    except OSError as e:
        print("Failed to read from SHT3x sensor, retrying...", e)
        sht_humidity, sht_temp = 0, 0  # Default values in case of read failure

    temp = (bme_temp + sht_temp) / 2
    pressure = bme_pressure
    humidity = (bme_humidity + sht_humidity) / 2
    payload = {
        'Humidity[%]': humidity,
        'TVOC[ppb]': 0,
        'eCO2[ppm]': 0,
        'Raw H2': 0,
        'Raw Ethanol': 0,
        'Pressure[hPa]': pressure
    }

    # Send POST request
    try:
        response = urequests.post(url, json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                print('Success:', data.get('message', 'Data received successfully'))
            except ValueError:
                print('Received non-JSON response:', response.text)
        else:
            print(f'Failed to send data, status code: {response.status_code}, Response: {response.text}')
        response.close()
    except Exception as e:
        print(f'Failed to send data: {str(e)}')

    sleep(10)
