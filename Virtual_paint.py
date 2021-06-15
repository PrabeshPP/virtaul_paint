import cv2 as cv
import numpy as np
cap=cv.VideoCapture(0) #opens the cam

my_colors=[[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255],
            [90, 48, 0, 118, 255, 255]]
RBG_Colors=[[51, 153, 255],  ## BGR
                 [255, 0, 255],
                 [0, 255, 0],
                 [255, 0, 0]]
my_points=[]


def find_color(frame,my_colors,RBG_Colors):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    count=0
    points=[]
    for my_colors in my_colors:
        lower_bound=np.array(my_colors[0:3])
        upper_bound=np.array(my_colors[3:6])
        mask=cv.inRange(hsv,lower_bound,upper_bound)
        x,y=get_contours(mask)
        cv.circle(frame1, (x, y), 20, RBG_Colors[count],cv.FILLED)
        if x!=0 and y!=0:
            points.append([x,y,count])
        count+=1
    return points

def get_contours(mask):
    contours,hierarchy=cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:

        peri=cv.arcLength(cnt,True)
        approximate=cv.approxPolyDP(cnt,peri*0.02,True)
        x,y,w,h=cv.boundingRect(approximate)
    return x+w//2,y

def plt_points(my_points,rbg_colors):
    for points in my_points:
        cv.circle(frame1,(points[0],points[1]),15,rbg_colors[points[2]],cv.FILLED)



while True:
    ret,frame=cap.read() #Read the frame one by one
    frame=cv.flip(frame,1)
    frame1=frame.copy() # created a new copy  of the frame each time it is read in the above line of code
    new_points=find_color(frame,my_colors,RBG_Colors)
    if len(new_points)!=0:
        for points in new_points:
            my_points.append(points)
    if len(my_points)!=0:
        plt_points(my_points,RBG_Colors)

    cv.imshow("Virtual_painting ",frame1)
    if cv.waitKey(1)==ord('q'):
        break
cap.release()
cv.destroyAllWindows()
