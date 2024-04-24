from machine import Pin, ADC
import utime
import math

# Hardware Related Macros
MQ_PIN = 33  # define which ADC input channel you are going to use
RL_VALUE = 10  # define the load resistance on the board, in kilo ohms
RO_CLEAN_AIR_FACTOR = 9.21  # derived from the chart in datasheet

# Software Related Macros
CALIBRATION_SAMPLE_TIMES = 50  # samples in the calibration phase
CALIBRATION_SAMPLE_INTERVAL = 500  # time interval (in ms) between samples in the calibration phase
READ_SAMPLE_INTERVAL = 50  # time interval (in ms) between samples in normal operation
READ_SAMPLE_TIMES = 5  # samples in normal operation

# Application Related Macros
GAS_H2 = 0

# Globals
H2Curve = [2.3, 0.93, -1.44]  # data format: {x, y, slope}
Ro = 10  # Ro initialized to 10 kilo ohms

def setup():
    print("Calibrating...")
    adc = ADC(Pin(MQ_PIN))
    adc.atten(ADC.ATTN_11DB)  # for ESP32, configure attenuation for full range
    global Ro
    Ro = MQCalibration(adc)
    print("Calibration is done...")
    print("Ro={0:.2f}kohm".format(Ro))

def loop():
    adc = ADC(Pin(MQ_PIN))
    adc.atten(ADC.ATTN_11DB)  # ensure attenuation is set for each read if necessary
    print("H2: {:.2f} ppm".format(MQGetGasPercentage(MQRead(adc) / Ro, GAS_H2)))
    utime.sleep_ms(200)

def MQResistanceCalculation(raw_adc):
    return (RL_VALUE * (4095 - raw_adc) / raw_adc) if raw_adc != 0 else 0

def MQCalibration(adc):
    val = 0
    for i in range(CALIBRATION_SAMPLE_TIMES):
        raw_adc = adc.read()
        val += MQResistanceCalculation(raw_adc)
        utime.sleep_ms(CALIBRATION_SAMPLE_INTERVAL)
    val /= CALIBRATION_SAMPLE_TIMES
    val /= RO_CLEAN_AIR_FACTOR
    return val

def MQRead(adc):
    rs = 0
    for i in range(READ_SAMPLE_TIMES):
        raw_adc = adc.read()
        rs += MQResistanceCalculation(raw_adc)
        utime.sleep_ms(READ_SAMPLE_INTERVAL)
    rs /= READ_SAMPLE_TIMES
    return rs

def MQGetGasPercentage(rs_ro_ratio, gas_id):
    if gas_id == GAS_H2:
        return MQGetPercentage(rs_ro_ratio, H2Curve)
    return 0

def MQGetPercentage(rs_ro_ratio, pcurve):
    x = (math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2] + pcurve[0]
    return math.pow(10, x)

# Main execution check
if __name__ == "__main__":
    setup()
    while True:
        loop()
