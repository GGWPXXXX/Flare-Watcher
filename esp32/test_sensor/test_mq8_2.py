from machine import ADC, Pin
import time
import math

my_pin = 33
RL_VALUE = 10  # define the load resistance on the board, in kilo ohms
R0_CLEAN_AIR_FACTOR = 9.21  # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO, which is derived from the chart in datasheet

CALIBARAION_SAMPLE_TIMES  = 50 # define how many samples you are going to take in the calibration phase
CALIBRATION_SAMPLE_INTERVAL = 500 # define the time interal(in milisecond) between each samples in the cablibration phase

READ_SAMPLE_INTERVAL = 50 # define how many samples you are going to take in normal operation
READ_SAMPLE_TIMES = 5 # define the time interal(in milisecond) between each samples in normal operation

GAS_H2 = 0

H2Curve = [2.3, 0.93,-1.44]

# two points are taken from the curve in datasheet. 
# with these two points, a line is formed which is "approximately equivalent" 
# to the original curve. 
# data format:{ x, y, slope}; point1: (lg200, lg8.5), point2: (lg10000, lg0.03)

R0 = 10 # Ro is initialized to 10 kilo ohms

adc = ADC(Pin(my_pin)) # ...

def MQResistanceCalculation(raw_adc : int):
    return  RL_VALUE * (4095 - raw_adc) / raw_adc

def MQCalibration():
    val = 0
    for i in range(CALIBARAION_SAMPLE_TIMES):
        val += MQResistanceCalculation(adc.read())
        time.sleep(CALIBRATION_SAMPLE_INTERVAL/1000) # in millisec
        
    val = val/CALIBARAION_SAMPLE_TIMES; # calculate the average value
    val = val/R0_CLEAN_AIR_FACTOR # divided by RO_CLEAN_AIR_FACTOR yields the Ro, according to the chart in the datasheet
    
    return val

def MQRead():
    Rs = 0
    for i in range(READ_SAMPLE_INTERVAL):
        Rs += MQResistanceCalculation(adc.read())
        time.sleep(READ_SAMPLE_INTERVAL/1000)
        
    Rs = Rs/READ_SAMPLE_TIMES
    return Rs

def MQGetGasPercentage(rs_ro_ratio : float, gas_id : int):
    if (gas_id == GAS_H2):
        return MQGetPercentage(rs_ro_ratio,H2Curve)
    else:
        return 0

def MQGetPercentage(rs_ro_ratio : float, pcurve : list):
    return math.pow(10, (((math.log10(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0]))
    
    

    
def setup()
    
    
    
    
