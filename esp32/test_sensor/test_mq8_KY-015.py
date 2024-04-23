from machine import ADC, Pin
import time

# Replace 'XX' with the actual pin number the MQ-8 sensor is connected to
sensor_pin = 33
adc = ADC(Pin(sensor_pin))
adc.atten(ADC.ATTN_11DB)  # Configure the attenuation for full range of 0-3.3V

def read_mq8_sensor():
    value = adc.read()
    print("MQ-8 Sensor Value:", value)
    # Optionally, you can add a conversion from the raw value to a concentration value here
    # This will require calibration with known concentrations of hydrogen gas

while True:
    read_mq8_sensor()
    time.sleep(1)  # Read sensor every second
