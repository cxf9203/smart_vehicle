import serial
import time
import threading
ser = serial.Serial("COM3",9600,timeout=0.5)
ser.flushInput()
def serial_read():

    count = ser.inWaiting()
    if count != 0:
        recv = ser.read(ser.in_waiting).decode("utf-8")
        print(time.time()," --- recv --->",recv)
    time.sleep(1)

def serial_send(text):
    ser.write((text + '\r\n').encode())

class serial_read(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        while 1:
            count = ser.inWaiting()
            if count != 0:
                recv = ser.readline().decode("gbk")
                print("distance is ",recv)


thread_serialread = serial_read("0","serial read")
thread_serialread.start()

if __name__ == '__main__':
    while 1:
        time.sleep(1)



