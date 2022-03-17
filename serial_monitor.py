import serial
import time

serialPort = "COM9"  # 串口
baudRate = 9600  # 波特率
ser = serial.Serial(serialPort, baudRate, timeout=0.5)
print("参数设置：串口=%s ，波特率=%d" % (serialPort, baudRate))


while 1:
    line = ser.readline().decode()
    sensorvalue = int(line[9:13])
    output = int(line[24:27])
    lightsensor = int(line[41:45])
    temp = int(line[52:57])

    time.sleep(0.5)
    print(line)
    print(sensorvalue)
    print(output)
    print(lightsensor)
    print(temp)
    print(type(sensorvalue))



ser.close
