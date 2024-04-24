from lib.sgp30 import Adafruit_SGP30
from machine import I2C, Pin
from time import sleep
i2c = I2C(1, sda=Pin(4), scl=Pin(5))
sgp30 = Adafruit_SGP30(i2c)
while(True):
    co2eq, tvoc = sgp30.iaq_measure()
    print("CO2eq = %d ppm \t TVOC = %d ppb" % (co2eq, tvoc))
    sleep(1)