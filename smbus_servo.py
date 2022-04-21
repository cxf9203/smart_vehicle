# -*- coding: utf-8 -*-
import serial
import time
serialPort="/dev/ttyUSB0"
baudRate = 115200
ser = serial.Serial(serialPort,baudRate,timeout=0.5)    ###serial = serial.Serial(serialPort,baudRate,timeout=0.5)


#ser.write(b'\r\n\r\n')
time.sleep(2)
ser.write(('#004P1200T1000!').encode())
time.sleep(0.5)

line = ser.readline()
out = line.decode('utf-8')
print(line)


ser.close()
