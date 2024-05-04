import serial
import time
ser = serial.Serial('COM4',115200)
s = [0,1] 
list = []
'''
Keep while True:
'''
def get_reading():
    read_serial=ser.readline().decode().strip()
    return read_serial
