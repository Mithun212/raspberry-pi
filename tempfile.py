import os
import glob
import time
import csv
from datetime import datetime

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Set up the location of the sensor in the system
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# CSV file to store data
csv_filename = 'temperature_log.csv'

# Check if the CSV file already exists, and create it with headers if it doesn't
if not os.path.isfile(csv_filename):
    with open(csv_filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Temperature (°C)'])

def read_temp_raw():
    with open(device_file, 'r') as f:
        valid, temp_line = f.readlines()
    return valid, temp_line

def read_temp():
    valid, temp_line = read_temp_raw()
    while 'YES' not in valid:
        time.sleep(0.2)
        valid, temp_line = read_temp_raw()
    equals_pos = temp_line.find('t=')
    if equals_pos != -1:
        temp_string = temp_line[equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def log_temperature_to_csv(temperature):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(csv_filename, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, temperature])

try:
    while True:
        temperature = read_temp()
        print(f'Current temperature: {temperature:.2f}°C')
        log_temperature_to_csv(temperature)
        time.sleep(1)  # Adjust the interval as needed (e.g., every 1 seconds)
except KeyboardInterrupt:
    print('Logging stopped by user.')
