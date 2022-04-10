import serial
import time

serialPort = "COM3"  # 串口
baudRate = 9600  # 波特率
ser = serial.Serial(serialPort, baudRate, timeout=0.5)
print("参数设置：串口=%s ，波特率=%d" % (serialPort, baudRate))


while 1:
    if ser.in_waiting:
        str1 = ser.readline().decode("gbk")

        print(str1)




