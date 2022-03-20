import cv2 as cv


# Initialize webcam feed
video = cv.VideoCapture("lane.mp4")
ret = video.set(3,640)
ret = video.set(4,480)



while 1:
    _,frame =video.read()
    gray = cv.cvtColor(frame,cv.COLOR_RGB2GRAY)
    _,thresh1 = cv.threshold(gray,70,255,cv.THRESH_BINARY)
    Path_Detct_fre_count = 1
    for j in range(0,640,5):
        if thresh1[240,j]==0:
            Path_Detct_px_sum=Path_Detct_px_sum+j

