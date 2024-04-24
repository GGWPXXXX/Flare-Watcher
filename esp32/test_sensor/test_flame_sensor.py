import math
from machine import Pin, ADC
import time

flame_sensor = Pin(33, Pin.IN)
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)

while(True):
    flame_detected = flame_sensor.value()
    value = adc.read()  # ESP32 uses adc.read()
    print("ADC Value:", value)
    print(f"value = {flame_detected}")
    time.sleep(1)