import serial
 
ser = serial.Serial('/dev/ttyACM0',115200)
s = [0,1] 
list = []
'''
Keep while True:
'''
def get_reading():
    read_serial=ser.readline().decode().strip()
    if read_serial.startswith('BPM: '):
        bpm_value=read_serial.replace('BPM: ','')
        print(bpm_value)
    s[0] = str(int (ser.readline(),16))
    return read_serial
