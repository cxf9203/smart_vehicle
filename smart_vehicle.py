#{
 # "ProductKey": "a1dlQQU7qPx",
  #"DeviceName": "vehicle_1",
  #"DeviceSecret": "c5524cb2c3232cadde7affc267960a88"
#}
#!/usr/bin/python3

import aliLink,mqttd     # pip install paho-mqtt -i https://mirrors.aliyun.com/pypi/simple/ 复制链接在终端shell或者terminal中安装mqttd
import time,json
import RPi.GPIO as GPIO

#board pin mode set
GPIO.setmode(GPIO.BCM)

#servo motor setting
#set pin 12(bcm) as servo pin 
GPIO.setup(12,GPIO.OUT)
servo1=GPIO.PWM(12,50) #50 = 50HZ PULSE
#set pin 6(bcm) as servo pin 
GPIO.setup(6,GPIO.OUT)
servo2=GPIO.PWM(6,50) #50 = 50HZ PULSE
#set pin 5(bcm) as servo pin 
GPIO.setup(5,GPIO.OUT)
servo3=GPIO.PWM(5,50) #50 = 50HZ PULSE

#initial servo
servo1.start(0)
servo2.start(0)
servo3.start(0)
print("waiting for 2 seconds")
time.sleep(2)
#motor drive set
ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26

#intialize motor drive
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
#motion function
#forward function
def motor_forward():
	print("motor forward")
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#motor_stop function
def motor_stop():
	print("motor backward")
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(ENA,False)
	GPIO.output(ENA,False)
	GPIO.output(ENA,False)
	GPIO.output(ENA,False)
	time.sleep(1)

#backward_function
def motor_backward():
	print("motor backward")
	GPIO.output(ENA,True)
	GPIO.output(ENA,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#turnleft_function
def motor_left():
	print("motor left")
	GPIO.output(ENA,True)
	GPIO.output(ENA,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	time.sleep(0.5)
#turnright_function
def motor_right():
	print("motor left")
	GPIO.output(ENA,True)
	GPIO.output(ENA,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	time.sleep(0.5)




#servo motor function
#dc-2-12,better 4-11
def servo_1(dc):
	servo1.ChangeDutyCycle(dc)
	time.sleep(0.3)
	servo1.ChangeDutyCycle(0)
	time.sleep(0.7)

def servo_2(dc):
	servo2.ChangeDutyCycle(dc)
	time.sleep(0.3)
	servo2.ChangeDutyCycle(0)
	time.sleep(0.7)
	
def servo_3(dc):
	servo3.ChangeDutyCycle(dc)
	time.sleep(0.3)
	servo3.ChangeDutyCycle(0)
	time.sleep(0.7)

# 三元素（iot后台获取）
ProductKey = 'a1dlQQU7qPx'
DeviceName = 'vehicle_1'
DeviceSecret = "c5524cb2c3232cadde7affc267960a88"
# topic (iot后台获取)
POST = '/sys/a1dlQQU7qPx/vehicle_1/thing/event/property/post'  # 上报消息到云
POST_REPLY = '/sys/a1dlQQU7qPx/vehicle_1/thing/event/property/post_reply'
SET = '/sys/a1dlQQU7qPx/vehicle_1/thing/service/property/set'  # 订阅云端指令



# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
	print(msg.payload)
	Msg = json.loads(msg.payload.decode('utf-8'))
	#callback Message from cloud
    
	#call back for axis_1	
	if ('axis_1' in Msg["params"].keys()):
		print("axis_1 is received")
		degree_1 = Msg['params']['axis_1']
		print("begin rotate axis_1 to ",degree_1)
		servo_1(degree_1)
	else:
		pass
	#call back for axis_2	
	if ('axis_2' in Msg["params"].keys()):
		print("axis_2 is received")
		degree_2 = Msg['params']['axis_2']
		print("begin rotate axis_2 to ",degree_2)
		servo_2(degree_2)
	else:
		pass
	#call back for axis_3	
	if ('axis_3' in Msg["params"].keys()):
		print("axis_3 is received")
		degree_3 = Msg['params']['axis_3']
		print("begin rotate axis_3 to ",degree_3)
		servo_3(degree_3)
	else:
		pass
	#call back for forward	
	if ('motiontask' in Msg["params"].keys()):
		print("motiontask is received")
		motion_num= Msg['params']['motiontask']
		if motion_num==1:
			motor_forward()
		elif motion_num==0:
			motor_stop()
		elif motion_num==2:
			motor_backward()
		elif motion_num==3:
			motor_left()
		elif motion_num==4:
			motor_right()
		else:
			motor_stop()
	else:
		pass
	print(msg.payload)
#连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
	pass


# 链接信息
Server,ClientId,userNmae,Password = aliLink.linkiot(DeviceName,ProductKey,DeviceSecret)

# mqtt链接
mqtt = mqttd.MQTT(Server,ClientId,userNmae,Password)
mqtt.subscribe(SET) # 订阅服务器下发消息topic
mqtt.begin(on_message,on_connect)


# 信息获取上报，每10秒钟上报一次系统参数
while True:
    time.sleep(20)
    # 构建与云端模型一致的消息结构
    updateMsn = {
        #'cpu_temperature':CPU_temp,
       # 'DISK_used_percentage':DISK_perc,
       # 'PowerLed':power_LED

    }
    JsonUpdataMsn = aliLink.Alink(updateMsn)
    print(JsonUpdataMsn)

    mqtt.push(POST,JsonUpdataMsn) # 定时向阿里云IOT推送我们构建好的Alink协议数据
