import cv2
from skimage import morphology
import numpy as np
import os
import time
import glob
import math





from get_file import get_imgs
from center import *


def simple_show(img,name='lol',time=1000):
    cv2.imshow(name,img)
    cv2.waitKey(time)


def get_part(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([50, 0, 100])
    up = np.array([100, 255, 255])
    mask = cv2.inRange(hsv, low, up)
    part = cv2.bitwise_and(hsv, hsv, mask=mask)
    return part
def color_reverse(gray):
    for i in range(len(gray)):
        for j in range(len(gray[0])):
            gray[i][j] = 255 - gray[i][j]
    return gray

images = get_imgs('./yellow')
KERNEL=np.ones((7,7), np.uint8)
cv2.namedWindow('lol')
cv2.moveWindow("lol", 20,20);
for i in range(len(images)):
    img = images[i]
    img = cv2.resize(img,(img.shape[1]//4,img.shape[0]//4))
    imgc = img
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    gray=img[:,:,2]
    gray=cv2.equalizeHist(gray)
    img[:,:,2]=gray[:,:,]
    img=cv2.cvtColor(img,cv2.COLOR_HSV2BGR)

    img = get_part(img)
    imgs = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)





    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    img = color_reverse(img)
    simple_show(img)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    _,th1 = cv2.threshold(th2,127,255,cv2.THRESH_BINARY_INV)
    th2 = cv2.erode(th1,KERNEL)
    th2 = cv2.dilate(th1,KERNEL)
    th2 = cv2.Canny(th1,200,200)
    th2 = cv2.adaptiveThreshold(th2,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    _,th2 = cv2.threshold(th2,127,255,cv2.THRESH_BINARY_INV)
    th2 = cv2.erode(th1,KERNEL)
    th2 = cv2.dilate(th1,KERNEL)
    chull = morphology.convex_hull_object(th2).astype(np.uint8) * 255
    _, contours, _ = cv2.findContours(chull, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # rect = cv2.minAreaRect(c)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # imgc=cv2.drawContours(imgc,[box],0,(0,0,255),2)



        (x,y),r = cv2.minEnclosingCircle(c)
        x, y, r = (int(i) for i in [x, y, r])
        circle = [x,y,r]
        imgc = draw_circle(imgc,circle)




    simple_show(th2)
    simple_show(imgc)
