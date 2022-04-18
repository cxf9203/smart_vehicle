import RPi.GPIO as GPIO
import time
import threading



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IRLEFT=27
IRRIGHT=18
CROSSDETECT_LEFT = 22
CORSSDETECT_RIGHT = 23

def left_Value():
    return GPIO.input(IRLEFT)
def right_Value():
    return GPIO.input(IRRIGHT)
def CROSSleft_Value():
    return GPIO.input(CROSSDETECT_LEFT)
def CROSSright_Value():
    return GPIO.input(CORSSDETECT_RIGHT)
#INITAIL PIN
def setup_dev():
    GPIO.setup(IRLEFT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(IRRIGHT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CROSSDETECT_LEFT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CORSSDETECT_RIGHT,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def destroy():
    GPIO,cleanup()
class get_IR(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.id = threadID
        self.name = name
    def run(self):
        setup_dev()
        try:
            while 1:
                self.left_IRsensor=left_Value()
                self.right_IRsensor=right_Value()
                self.crossleft_IRsensor=CROSSleft_Value()
                self.crossright_IRsensor=CROSSright_Value()
                time.sleep(0.5)
        except KeyboardInterrupt:
            destroy()
get_irsensor = get_IR("1","get_IRsensor")
get_irsensor.start()
if __name__=="__main__":
    #initial
    cross_count=0
    
    while 1:
        if (get_irsensor.crossleft_IRsensor==0 &get_irsensor.left_IRsensor==1 & get_irsensor.right_IRsensor==1&get_irsensor.crossright_IRsensor==0):#xiaoche zai heixian shang
            print("qian jin forward")
        if (get_irsensor.left_IRsensor==1 & get_irsensor.right_IRsensor==0):#xiaoche youpian
            print("xiaoche zuozhuan")
            time.sleep(0.1)
        if (get_irsensor.left_IRsensor==0 & get_irsensor.right_IRsensor==1):#xiaoche zuopian
            print("xiaoche youzhuan")
            time.sleep(0.1)
        if (get_irsensor.crossleft_IRsensor==0 &get_irsensor.left_IRsensor==1 & get_irsensor.right_IRsensor==1&get_irsensor.crossright_IRsensor==0):#xiaoche zai cross lukou
            print("jinxing panduan")
            cross_count = cross_count+1
            if cross_count==1:
                print("xiaoche zuozhuan")
                print("callback process")
            if (cross_count==8 or cross_count==17 or cross_count==26 or cross_count==35 or cross_count==37 ):#chaoshengbo fuzhu youzhuan?
                print("youzhuan xiaoche")
            else:
                #zhuaqu wujian
                #todo
                print("zhunbei zhuaqu")
                
            
                
