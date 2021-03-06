import cv2 as cv
import RPi.GPIO as GPIO
import time
import threading
import sys
import numpy as np
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
#set pin 27(bcm) as servo pin for drive
GPIO.setup(27,GPIO.OUT)
servo4=GPIO.PWM(27,50) #50 = 50HZ PULSE

#initial servo
servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)
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
    print("motor stop")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
    time.sleep(1)


# backward_function
def motor_backward():
    print("motor backward")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


# turnleft_function
def motor_right():
    print("motor right")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    time.sleep(0.5)


# turnright_function
def motor_left():
    print("motor left")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
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
def servo_4_guide(theta):
    servo4.ChangeDutyCycle(theta)
    time.sleep(0.3)
    servo4.ChangeDutyCycle(0)
    time.sleep(0.2)
#????????????motor set
def lane_following(Lmotor_speed,Rmotor_speed,t_time):
    #????????????
    ENA_PWM.ChangeDutyCycle(Lmotor_speed)
    #????????????
    ENB_PWM.ChangeDutyCycle(Rmotor_speed)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    time.sleep(t_time)


# Initialize webcam feed
video = cv.VideoCapture(0)#0 or video lane.mp4
print(video.get(3))#1280 picamera 640
print(video.get(4))#720  480

#PID???????????????
kp=0.85
ki=0
kd=0
ref_center=640/2
last_err=0
total_err= 0 #??????
pid_output=0

def activator(u):
    u_l=70+1.2*u
    u_r=70-1.2*u
    #??????????????????
    if u_l>95:
        u_l=95
    if u_r>95:
        u_r=95
    #?????????????????????0
    if u_l<=0:
        u_l=0
    if u_r<=0:
        u_r=0
    lane_following(u_l,u_r,0)

def servo_guide(u):
    theta=7+u/10
    if theta>11:
        theta=11
    if theta<4:
        theta=4
    servo_4_guide(theta)
#todo another threading
#????????????????????????
cols = video.get(3)#??????
rows = video.get(4)#??????
print(cols)
horizontal_size = 30
# Create structure element for extracting horizontal lines through morphology operations
horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
#???????????????
mask = np.zeros((int(rows),int(cols),1),dtype="uint8")
cv.rectangle(mask,(5,25),(100,200),255,-1)
cv.rectangle(mask,(int(cols)-5,20),(int(cols-105),200),255,-1)
#cv.imshow("mask",mask)
#mask and ????????? ?????????
kernel = np.ones((5,5),np.uint8)
Path_Detct_px_sum = 0 #???????????????
threadLock = threading.Lock()
threads = []
while 1:
    ret,frame =video.read()
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    # _,thresh1 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    _, thresh1 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # cv.imshow("thresh_BI_bw_not", thresh1)
    cross_detect_img = cv.bitwise_and(thresh1, mask)
    # cross_detect_img = cv.erode(cross_detect_img,kernel,iterations=1)
    # cross_detect_img = cv.dilate(cross_detect_img, kernel, iterations=1)
    cv.imshow("cross_detect", cross_detect_img)
    contours, hierarchy = cv.findContours(cross_detect_img, cv.RETR_EXTERNAL,
                                          cv.CHAIN_APPROX_NONE)  # ???????????????????????????
    # print(contours)
    s = 0
    area = [None] * len(contours)
    for i, c in enumerate(contours):
        M = cv.moments(c)
        area[i] = M['m00']
        s = area[i] + s
    print(s)
    if s < 30000:
        print("cross detected \n stop motor \n __________")
        # todo
        print("motor left fcn")
        time.sleep(1)
    else:
        pass


    Path_Detct_fre_count = 1
    for j in range(0,640,5):
        if thresh1[200,j]==0:
            Path_Detct_px_sum=Path_Detct_px_sum+j
            Path_Detct_fre_count = Path_Detct_fre_count+1
    Path_Detect_px = int((Path_Detct_px_sum)/(Path_Detct_fre_count))
    cv.circle(frame,(Path_Detect_px,200),10,(0,255,0),thickness=2)
    cv.imshow("reference point",frame)
    #cv.imshow("gray",gray)
    #cv.imshow("thresh",thresh1)
    if cv.waitKey(1)&0XFF==ord('q'):
        motor_stop()
        break
    #pid function
    current_err= ref_center-Path_Detect_px
    print("current error is :",current_err)
    total_err=total_err+current_err
    pid_output= kp*current_err+ki*total_err+kd*(current_err-last_err) #??????????????t?????????kd???ki???????????????????????????????????????????????????
    # ??????????????????????????????????????????
    last_err=current_err
    u=pid_output #??????????????????????????????
    #???????????????????????????u
    #motot drive guide
    activator(u)
    #servo_guide
    #servo_guide(u)
    #initialize
    Path_Detct_px_sum = 0
video.release()
cv.destroyAllWindows()

