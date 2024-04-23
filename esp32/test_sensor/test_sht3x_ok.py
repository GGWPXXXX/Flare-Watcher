from machine import I2C, Pin
from time import sleep_ms
from lib.sht3x import SHT3x

# Setup I2C
i2c = I2C(1, sda=Pin(4), scl=Pin(5))
detected_devices = i2c.scan()
print("Detected I2C addresses:", [hex(addr) for addr in detected_devices])

# Assuming the SHT3x is detected at either 0x44 or 0x45
if 0x44 in detected_devices:
    address = 0x44
elif 0x45 in detected_devices:
    address = 0x45
else:
    print("SHT3x not detected. Check connections.")
    while True:
        sleep_ms(1000)  # Halt the program, continually delaying

# Initialize SHT3x with correct address
sht30 = SHT3x(i2c, addr=address)

# Main loop to measure and print humidity and temperature
while True:
    try:
        sht30.measure()
        sht_humidity, sht_temp = sht30.ht()
        print(f"Humidity: {sht_humidity}%, Temperature: {sht_temp}°C")
    except OSError as e:
        print("Failed to read from sensor, retrying...", e)
    sleep_ms(1000)
