from machine import Pin, I2C
from time import sleep
from lib.bme280 import BME280, BME280_OSAMPLE_2, BME280_I2CADDR

# Setup I2C
i2c = I2C(1, sda=Pin(4), scl=Pin(5))
print(i2c.scan())  # This should show the I2C address of the BME280 if it's connected correctly.

# Initialize BME280
bme280 = BME280(mode=BME280_OSAMPLE_2, address=BME280_I2CADDR, i2c=i2c)

# Loop to print human-readable sensor data
while True:
    temperature, pressure, humidity = bme280.read_compensated_data()
    temperature = temperature / 100.0  # Convert to Celsius
    pressure = pressure / 25600.0      # Convert to hPa
    humidity = humidity / 1024.0       # Convert to %

    print(f'Temperature: {temperature} °C, type={type(temperature)}')
    print(f'Pressure: {pressure} hPa, type={type(pressure)}')
    print(f'Humidity: {humidity} %, type={type(humidity)}')
    print('-----------------------------------------------')
    sleep(1)  # Sleep for 1 second
