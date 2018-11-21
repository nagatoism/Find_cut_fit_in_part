# -*- coding: utf-8 -*-
"""
Created on Tue Jul 03 09:42:56 2018

@author: xern5
"""

import cv2
from skimage import morphology
import numpy as np
import os
import time
import glob
import math

def find_contour(contours, area=200):
    contour = None
    for cnt in contours:
        cnt = cnt[:, 0, :]
        if cv2.contourArea(cnt) > area:
            if contour is None:
                contour = cnt
            else:
                contour = np.concatenate((contour, cnt))
    return contour

def get_part(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([30, 10, 0])
    up = np.array([180, 60, 255])
    mask = cv2.inRange(hsv, low, up)
    part = cv2.bitwise_and(hsv, hsv, mask=mask)
    return part
def get_edges(bgr): # 找边缘
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(bgr, kernel, iterations=1)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    edgs = cv2.Canny(gray, 100, 200)
    return edgs

def get_en_circle(edgs): # 画外接圆
    chull = morphology.convex_hull_object(edgs).astype(np.uint8) * 255
    _, contours, _ = cv2.findContours(chull, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = find_contour(contours)
    (x, y), r = cv2.minEnclosingCircle(contour)
    x, y, r = (int(i) for i in [x, y, r])
    circle=[x,y,r]
    return circle


def draw_circle(img,circle): #画一个圆形
    x=circle[0];y=circle[1];r=circle[2]
    img = cv2.circle(img, (x,y), r, (0,0,255))
    img= cv2.circle(img, (x,y), 2, (0,0,255))
    return img

def read_parts(): #读取小样
        parts = []
        f_list1=glob.glob('./parts/*.jpg')
        f_list2=glob.glob('./parts/*.png')
        f_list=f_list1+f_list2

        for file in f_list:
            image = cv2.imread(file)
            image = cv2.resize(image, (image.shape[1]//4, image.shape[0]//4))
            part = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            parts.append(part)
        return parts


def get_loc( gray,parts): # 找最匹配的小样
    res=[]
    for i in range(len(parts)):

        prob = cv2.matchTemplate(gray, parts[i], cv2.TM_CCOEFF_NORMED)
        maxp = prob.max()
        loc = np.where(prob == maxp)
        h, w = int(part.shape[0]), int(part.shape[1])
        res.append((maxp, loc[1][0], loc[0][0], w, h))
    res.sort(key=lambda x: x[0], reverse=True)
    return res  [0][1:]

def draw(img,circle,rec):
    x1=circle[0]
    y1=circle[1]
    x2=(2*x+w)//2
    y2=(2*y+h)//2
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0))
    x3=x1+(x2-x1)*0.618
    y3=y2+(y2-y1)*0.618
    # r2=int(math.sqrt(abs(x1-x3)**2+abs(y1-y3)**2))
    r2=60

    c2=[x1,y1,r2]
    img=draw_circle(img,c2)
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255))
    img=draw_circle(img,circle)
    return img


if __name__=='__main__':
    f_list=glob.glob('./1_three/*')
    parts=read_parts()
    t=0
    count=0
    for i in f_list:
        count+=1
        t1 = time.time()
        img = cv2.imread(i)
        f_name=i.split('/'  )[-1]
        img = cv2.resize(img, (img.shape[1]//4, img.shape[0]//4))
        part=get_part(img)
        bgr = cv2.cvtColor(part, cv2.COLOR_HSV2BGR)
        edgs=get_edges(bgr)
        circle=get_en_circle(edgs)


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x, y, w, h =get_loc( gray,parts)


        rec=[x,y,w,h]
        img=draw(img,circle,rec)
        t2=time.time()
        t+=t2-t1
        print(t2-t1)
        print('for one image')
        print(t/count)
        print('average time')
        cv2.imwrite('./small_res/'+f_name+'.png',img)
    #cv2.imwrite("result.jpg", img)
    #cv2.imshow('detected', img)
    #cv2.waitKey(0)
