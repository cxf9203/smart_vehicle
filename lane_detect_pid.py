import cv2 as cv
import RPi.GPIO as GPIO
import time
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
ENA_PWM=GPIO.PWM(ENA,1000)
ENA_PWM.start(0)
ENA_PWM.ChangeDutyCycle(80)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)


GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_PWM=GPIO.PWM(ENB,1000)
ENB_PWM.start(0)
ENB_PWM.ChangeDutyCycle(80)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)


def motor_forward():
    print("motor forward")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


# motor_stop function
def motor_stop():
    print("motor backward")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(ENA, False)
    GPIO.output(ENA, False)
    GPIO.output(ENA, False)
    GPIO.output(ENA, False)
    time.sleep(1)


# backward_function
def motor_backward():
    print("motor backward")
    GPIO.output(ENA, True)
    GPIO.output(ENA, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


# turnleft_function
def motor_left():
    print("motor left")
    GPIO.output(ENA, True)
    GPIO.output(ENA, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    time.sleep(0.5)


# turnright_function
def motor_right():
    print("motor left")
    GPIO.output(ENA, True)
    GPIO.output(ENA, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    time.sleep(0.5)


# servo motor function
# dc-2-12,better 4-11
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
#循迹前进motor set
def lane_following(Lmotor_speed,Rmotor_speed,t_time):
    #左轮设置
    ENA_PWM.ChangeDutyCycle(Lmotor_speed)
    #右轮设置
    ENB_PWM.ChangeDutyCycle(Rmotor_speed)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    time.sleep(t_time)


# Initialize webcam feed
video = cv.VideoCapture("lane.mp4")
print(video.get(3))#1280
print(video.get(4))#720

#PID参数初始化
kp=0.85
ki=0
kd=0
ref_center=1280/2
last_err=0
total_err= 0 #积分
pid_output=0

def activator(u):
    u_l=70+1.2*u
    u_r=70-1.2*u
    #双轮上限速度
    if u_l>95:
        u_l=95
    if u_r>95:
        u_r=95
    #双轮最小速度为0
    if u_l<=0:
        u_l=0
    if u_r<=0:
        u_r=0
    lane_following(u_l,u_r,0)



Path_Detct_px_sum = 0 #坐标值求和
while 1:
    ret,frame =video.read()
    gray = cv.cvtColor(frame,cv.COLOR_RGB2GRAY)
    _,thresh1 = cv.threshold(gray,60,255,cv.THRESH_BINARY)
    Path_Detct_fre_count = 1
    for j in range(0,1280,5):
        if thresh1[200,j]==0:
            Path_Detct_px_sum=Path_Detct_px_sum+j
            Path_Detct_fre_count = Path_Detct_fre_count+1
    Path_Detect_px = int((Path_Detct_px_sum)/(Path_Detct_fre_count))
    cv.circle(frame,(Path_Detect_px,200),10,(0,255,0),thickness=2)
    cv.imshow("reference point",frame)
    #cv.imshow("gray",gray)
    #cv.imshow("thresh",thresh1)
    if cv.waitKey(1)&0XFF==ord('q'):
        break
    #pid function
    current_err= ref_center-Path_Detect_px
    print(current_err)
    total_err=total_err+current_err
    pid_output= kp*current_err+ki*total_err+kd*(current_err-last_err) #实际中有Δt，由于kd和ki均为固定参数，且循环频率基本固定，
    # 可以直接等效为某一个固定值。
    last_err=current_err
    u=pid_output #输出值直接传递给速度
    #执行器采用该输出值u
    activator(u)
    #initialize
    Path_Detct_px_sum = 0
video.release()
cv.destroyAllWindows()

