import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time
import threading
import smbus

from modules.configuration import dashboard_config
from modules.structs import task
from modules.endpoints import send_push_notifications

thread_lock = threading.Lock()

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins
GPIO_TRIGGER = 14
GPIO_ECHO = 15
GPIO_RELAY = 22

# GPIO direction (IN / OUT)
GPIO.setup(GPIO_RELAY, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Ensure RELAY Pin is low
GPIO.output(GPIO_RELAY, GPIO.LOW)

#ADS1115 Object
adc = Adafruit_ADS1x15.ADS1115(address=0x49)

# ADS1115 address on the I2C bus
ADS1115_ADDRESS = 0x49

# Select the I2C bus (for Raspberry Pi 3, use '1' instead of '0')
bus = smbus.SMBus(1)

max_height_cm = 76
tank_max_level = 0.95

def relay_open():
    GPIO.output(GPIO_RELAY, GPIO.HIGH)

def relay_close():
    GPIO.output(GPIO_RELAY, GPIO.LOW)

def read_adc_value():
    adc_value = adc.read_adc(0, gain=1)
    return adc_value

def calculate_voltage(adc_value):
    voltage = adc_value / 32767.0 * 4.096
    return voltage

def voltage_to_liters(voltage):

    # Calibration values
    raw_empty = 900
    voltage_empty = 0
    liters_empty = 0

    raw_full = 28100
    voltage_full = 3.3
    liters_full = 1000

    liters = (voltage - voltage_empty) / (voltage_full - voltage_empty) * (liters_full - liters_empty) + liters_empty
    return liters

def measure_waterlevel():
    thread_lock.acquire()
    
    print("measuring waterlevel")
    adc_values = []
    for x in range(0,5):
        adc_value = read_adc_value()
        adc_values.append(adc_value)
        time.sleep(1)

    adc_average = list_average(adc_values)
    voltage = calculate_voltage(adc_average)
    liters = voltage_to_liters(voltage)
    waterlevel = liters / 1000
    thread_lock.release()
    return round(waterlevel,2)

def threshold_drain():

    #Ensure RELAY Pin is low
    GPIO.output(GPIO_RELAY, GPIO.LOW)

    #Retrieve Threshold from Global Drain_Threshold
    threshold = dashboard_config.drain_threshold
    current_level = measure_waterlevel()

    print("threshold-drain started")
    send_push_notifications("Tank Entwässerung gestartet!")

    #Keep Valve open until targetlevel reached
    while current_level > threshold and not task.drain_stopped:
        
        if not dashboard_config.is_draining:
            relay_open()
            dashboard_config.is_draining = True
        
        time.sleep(0.3)
        current_level = measure_waterlevel()

    relay_close()
    print("threshold-drain finished")
    send_push_notifications("Tank Entwässerung beendet!")

    dashboard_config.is_draining = False
    dashboard_config.waterlevel = current_level
    task.set_task("default",None)
    task.set_drain_stopped(False)

def list_average(ls):
    average = sum(ls)/len(ls)
    return average    

def old_read_adc(channel):
    config = [0x81, 0x83]  # Initial configuration
    #config[0] = 0x83  # Update the MUX and PGA bits for A0 and +/- 2.048V range

    # Write configuration data
    bus.write_i2c_block_data(ADS1115_ADDRESS, 1, config)

    # Wait for conversion to complete
    time.sleep(0.1)

    # Read ADC data
    data = bus.read_i2c_block_data(ADS1115_ADDRESS, 0, 2)
    raw_value = (data[0] << 8) + data[1]
    
    print("raw_value:",raw_value)

    voltage = (raw_value / 32767.0) * 4.096

    print("voltage:",voltage)

    return raw_value

def map_to_01(input_value):
    min_input = 0.0  # Minimum input value (0V)
    max_input = 3.0  # Maximum input value (3V)
    
    # Perform linear mapping
    output = (input_value - min_input) / (max_input - min_input)
    
    # Make sure the output is within the [0, 1] range
    output = max(0.0, min(1.0, output))
    
    return output