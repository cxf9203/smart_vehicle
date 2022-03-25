import cv2 as cv
import threading
import sys
import numpy as np
import time
def motor_stop():
    print("motor stop")
# Initialize webcam feed
video = cv.VideoCapture("lane.mp4")
#得到图像的宽和高
cols = video.get(3)#宽度
rows = video.get(4)#高度
print(cols)
horizontal_size = 30
# Create structure element for extracting horizontal lines through morphology operations
horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))

#todo another threading
#先创建掩膜
mask = np.zeros((int(rows),int(cols),1),dtype="uint8")
cv.rectangle(mask,(5,25),(100,200),255,-1)
cv.rectangle(mask,(int(cols)-5,20),(int(cols-105),200),255,-1)
#cv.imshow("mask",mask)
#mask and 二值化 位运算
kernel = np.ones((5,5),np.uint8)

#计算位运算的面积，大于某固定值则为检测到十字路口




#Apply morphology operations
def morpho(frame):
    horizontal = np.copy(frame)
    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)
    cv.imshow("horizantal", horizontal)


Path_Detct_px_sum = 0 #坐标值求和
threadLock = threading.Lock()
threads = []
if __name__ == '__main__':
    while 1:
        ret, frame = video.read()
        #print(frame.shape)
        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)


        # _,thresh1 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        _, thresh1 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # cv.imshow("thresh_BI_bw_not", thresh1)
        cross_detect_img = cv.bitwise_and(thresh1,mask )
        #cross_detect_img = cv.erode(cross_detect_img,kernel,iterations=1)
        #cross_detect_img = cv.dilate(cross_detect_img, kernel, iterations=1)
        cv.imshow("cross_detect", cross_detect_img)
        contours, hierarchy = cv.findContours(cross_detect_img, cv.RETR_EXTERNAL,
                                              cv.CHAIN_APPROX_NONE)  # 找到该对象外部轮廓
        #print(contours)
        s = 0
        area = [None] * len(contours)
        for i, c in enumerate(contours):
            M = cv.moments(c)
            area[i] = M['m00']
            s = area[i]+s
        print(s)
        if s < 30000:
            print("cross detected \n stop motor \n __________")
            #todo
            print("motor left fcn")
            time.sleep(1)
        else:
            pass
        Path_Detct_fre_count = 1
        for j in range(0, 1280, 5):
            if thresh1[300, j] == 0:
                Path_Detct_px_sum = Path_Detct_px_sum + j
                Path_Detct_fre_count = Path_Detct_fre_count + 1
        Path_Detect_px = int((Path_Detct_px_sum) / (Path_Detct_fre_count))
        #print(Path_Detect_px)
        # draw ref circle
        cv.circle(frame, (Path_Detect_px, 300), 10, (150, 255, 0), thickness=-1)
        #cv.imshow("reference point",frame)
        cv.circle(gray, (Path_Detect_px, 300), 10, 200, thickness=-1)
        #cv.imshow("gray", gray)
        #cv.imshow("thresh", thresh1)
        #退出判断
        if cv.waitKey(1) & 0XFF == ord('q'):
            break
        # initialize detect_px
        Path_Detct_px_sum = 0

    # quit
    video.release()
    cv.destroyAllWindows()
