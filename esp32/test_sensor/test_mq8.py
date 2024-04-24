import math
from machine import ADC, Pin
import time

# Calibration constants (replace with your actual calibration values)
m = -1.0  # Slope of the linear equation
b = 1.0   # Y-intercept of the linear equation
R0 = 10   # Sensor resistance in clean air (replace with your actual R0 value)

# Initialize ADC
# adc = ADC(Pin(33))  # Use ADC pin 0
adc = 124

def read_sensor_voltage():
    """
    Read analog output voltage from MQ-8 sensor.
    Returns:
        - Voltage: Analog output voltage from sensor
    """
    try:
        # Read ADC value (0-1023)
#         adc_value = adc.read()
        # Convert ADC value to voltage (0-3.3V)
        adc_value = 124
        voltage = adc_value * (3.3 / 4095)
        return voltage
    except Exception as e:
        print("Error reading sensor voltage:", e)
        return 0.0

def convert_voltage_to_resistance(voltage):
    """
    Convert analog output voltage to sensor resistance.
    Args:
        - voltage: Analog output voltage from sensor
    Returns:
        - Rs: Sensor resistance
    """
    try:
        # Calculate sensor resistance using voltage divider formula
#         Rs = (5 - voltage) / voltage * 10
        Rs =(voltage * 10000 / (5 - voltage))
    # Assuming load resistor is 10k ohms
        return Rs
    except Exception as e:
        print("Error converting voltage to resistance:", e)
        return 0.0

def calculate_hydrogen_concentration(Rs):
    """
    Calculate hydrogen gas concentration based on sensor resistance.
    Args:
        - Rs: Sensor resistance in the presence of hydrogen gas
    Returns:
        - Concentration: Estimated hydrogen gas concentration
    """
    try:
#         concentration = 10 ** ((math.log10(Rs / R0) - b) / m)
        concentration = 10 ** (-4.23 + 3.09*(math.log10(Rs / R0)))
        return concentration
    except ValueError:
        return 0.0  # Return 0 if Rs or R0 is zero or negative

if __name__ == "__main__":
    while(True):
        try:
            print("MQ-8 Hydrogen Gas Sensor Calibration")
            print("Please make sure the sensor is in a controlled environment with clean air.")
    #         input("Press Enter to start calibration...")

            # Measure sensor resistance in clean air
            print("Measuring sensor resistance in clean air...")
            clean_air_voltage = read_sensor_voltage()
            clean_air_Rs = convert_voltage_to_resistance(clean_air_voltage)
            print(f"Sensor Voltage in clean air: {clean_air_voltage} V")
            print(f"Sensor Resistance in clean air: {clean_air_Rs} kOhms")

    #         input("Place the sensor in a known concentration of hydrogen gas. Press Enter to measure...")

            # Measure sensor resistance in the presence of hydrogen gas
            print("Measuring sensor resistance in the presence of hydrogen gas...")
            gas_voltage = read_sensor_voltage()
            gas_Rs = convert_voltage_to_resistance(gas_voltage)
            print(f"Sensor Voltage in the presence of hydrogen gas: {gas_voltage} V")
            print(f"Sensor Resistance in the presence of hydrogen gas: {gas_Rs} kOhms")

            # Calculate hydrogen gas concentration
            concentration = calculate_hydrogen_concentration(gas_Rs)
            print(f"Estimated Hydrogen Gas Concentration: {concentration} ppm")

        except KeyboardInterrupt:
            print("\nCalibration process interrupted.")
        except Exception as e:
            print("Error during calibration:", e)
        time.sleep(2)
