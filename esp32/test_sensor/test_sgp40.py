import time
from machine import I2C, Pin
from sgp40 import SGP40

# Hypothetical calibration constants for the linear model
# These values need to be determined through empirical calibration
SCALE_FACTOR = 0.1  # Example scale factor
OFFSET = 5          # Example offset

def convert_voc_index_to_ppm(voc_index):
    """
    Convert raw VOC index to ppm using a hypothetical linear model.
    Adjust SCALE_FACTOR and OFFSET based on calibration data.
    """
    return voc_index * SCALE_FACTOR + OFFSET

# Initialize I2C communication
# Specify the SDA and SCL pins (Pin 4 for SDA, Pin 5 for SCL)
i2c = I2C(1, sda=Pin(4), scl=Pin(5))

# Scan for devices on the I2C bus to ensure the sensor is detected
print("Scanning I2C bus...")
devices = i2c.scan()
if 0x59 in devices:
    print("SGP40 sensor found at address 0x59")
else:
    print("SGP40 sensor not found. Check connections.")
    while True:
        pass  # Halt execution if sensor is not detected

# Initialize the SGP40 sensor
sgp40 = SGP40(i2c, 0x59)


# Continuously read, convert, and print the sensor output
while True:
    raw_value = sgp40.measure_raw()
    ppm_value = convert_voc_index_to_ppm(raw_value)
    print(f"Raw VOC measurement: {raw_value}, Converted VOC concentration: {ppm_value} ppm")
    time.sleep(1)  # Delay between measurements