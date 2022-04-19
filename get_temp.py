import time
while 1:
    time.sleep(10)
    file = open("/sys/class/thermal/thermal_zone0/temp")
    temp = float(file.read())/1000

    file.close()

    print(temp)

