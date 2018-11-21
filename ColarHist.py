import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import os
from get_patch import get_patch,get_center_patch
from algo import *

def ColarHist(img):
    color = ('b', 'g', 'r')

    HisColor = []
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        HisColor.append(histr)
    return HisColor
def compare(HisColor1,HisColor2):

    value = cv2.compareHist(HisColor1[0], HisColor2[0], cv2.HISTCMP_INTERSECT) + \
            cv2.compareHist(HisColor1[1], HisColor2[1], cv2.HISTCMP_INTERSECT) + \
            cv2.compareHist(HisColor1[2], HisColor2[2], cv2.HISTCMP_INTERSECT)
    return value

def find_match(imgSrc):
    besti=0
    bestj=0
    bestvalue=0
    values=[]
    STEP=10
    rowsSrc, colsSrc,_ = imgSrc.shape
    for i in range(0,rowsSrc-rows,STEP):
        for j in range(0,colsSrc-cols,STEP):
            sample=imgSrc[i:i+rows,j:j+cols,:]
            his_sample=ColarHist(sample)
            value=compare(his_sample,his_patch)


            if(value>bestvalue):
                besti = i
                bestj = j
                bestvalue = value
    loc_x1 = max(0,besti-STEP)
    loc_x2 = min(rowsSrc-cols,besti+STEP)
    loc_y1 = max(0,bestj-STEP)
    loc_y2 = min(colsSrc-cols,bestj+STEP)

    for i in range(loc_x1,loc_x2):
        for j in range(loc_y1,loc_y2):
            sample=imgSrc[i:i+rows,j:j+cols,:]
            his_sample=ColarHist(sample)
            value=compare(his_sample,his_patch)
            value=cv2.matchTemplate()

            if(value>bestvalue):
                besti = i
                bestj = j
                bestvalue = value


    res = imgSrc[besti:besti+rows,bestj:bestj+cols,:]
    return besti,bestj,res

def find_small_match(imgSrc):
    besti=0
    bestj=0
    bestvalue=0

    STEP=1
    rowsSrc, colsSrc,_ = imgSrc.shape
    for i in range(0,rowsSrc-s_rows,STEP):
        for j in range(0,colsSrc-s_cols,STEP):
            sample=imgSrc[i:i+s_rows,j:j+s_cols,:]
            his_sample=ColarHist(sample)
            value=compare(his_sample,his_s_patch)

            if(value>bestvalue):
                besti = i
                bestj = j
                bestvalue = value
    loc_x1 = max(0,besti-STEP)
    loc_x2 = min(rowsSrc-s_cols,besti+STEP)
    loc_y1 = max(0,bestj-STEP)
    loc_y2 = min(colsSrc-s_cols,bestj+STEP)

    for i in range(loc_x1,loc_x2):
        for j in range(loc_y1,loc_y2):
            sample=imgSrc[i:i+s_rows,j:j+s_cols,:]
            his_sample=ColarHist(sample)
            value=compare(his_sample,his_patch)

            if(value>bestvalue):
                besti = i
                bestj = j
                bestvalue = value


    res = imgSrc[besti:besti+s_rows,bestj:bestj+s_cols,:]
    return besti,bestj,res

def temp_match(imgSrc,pt):
    x1 = max(0,pt[0]-s_rows)
    y1 = max(0,pt[1]-s_cols)
    x2 = min(imgSrc.shape[0],pt[0]+s_rows)
    y2 = min(imgSrc.shape[1],pt[1]+s_cols)
    sample = imgSrc[x1:x2,y1:y2]
    if(x1-x2>=s_rows and y1-y2>=s_cols):
        res=cv2.matchTemplate(sample,small_img_gray,cv2.TM_CCOEFF_NORMED)
        loc=np.where(res==res.max())
        x = loc[0][0]
        y = loc[1][0]
        value = res[x,y]
    else:
        x = pt[0]
        y = pt[1]
        value = -1000
    return x,y,value
def dist(pt1,pt2):
    return (pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2


if __name__ == '__main__':

    img = cv2.imread('./color/yongkang.jpg', cv2.IMREAD_COLOR)
    img = cv2.resize(img, (img.shape[1]//2,img.shape[0]//2))
    # cv2.imshow('lat',img)
    # cv2.waitKey(5000)
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    small_img = cv2.imread('./color/cut_small.png', cv2.IMREAD_COLOR)
    small_img_gray=cv2.cvtColor(small_img,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('lat',small_img)
    # cv2.waitKey(5000)

    rows, cols, _ = img.shape
    s_rows, s_cols, _ = small_img.shape

    his_patch = ColarHist(img)
    # his_s_patch = ColarHist(small_img)



    # imgSrc=cv2.imread('p3.jpg')
    #
    # _,_,res=find_match(imgSrc)
    # small_res=find_math(res)
    KERNEL=np.ones((3,3),np.uint8)
    THRESHHOLD=0.65
    capVideo = cv2.VideoCapture(0)
    idx = 0
    pair_list =[]
    prepare_list =[]

    print(capVideo.get(cv2.CAP_PROP_FPS))
    while (capVideo.isOpened()):

        acc = time.time()
        idx+=1
        ret, frame = capVideo.read()

        frame_list = []

        if(ret==False):
            break
        else:
            pass
        if(idx%1==0):


            frame=cv2.resize(frame,(frame.shape[1]//2,frame.shape[0]//2))
            frame=get_center_patch(frame)
            frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            frame_gray = np.uint8(frame_gray)

            lap1 = time.time()-acc
            print('lap1',lap1)


            res = cv2.matchTemplate(frame_gray,img_gray,cv2.TM_CCOEFF_NORMED)
            loc = np.where((res==res.max()))

            lap1 = time.time()-acc
            print('lap1.5',lap1)


            x,y = loc[0][0],loc[1][0]
            pt=(x+rows//2,y+cols//2)

            cut_x_1 = max(0,pt[0]-110)
            cut_x_2 = min(pt[0]+110,frame.shape[0])
            cut_y_1 = max(0,pt[1]-110)
            cut_y_2 = min(pt[1]+110,frame.shape[1])
            dev_x = pt[0]-110
            dev_y = pt[1]-110
            print(dev_x,dev_y)
            c_cut =frame[cut_x_1:cut_x_2,cut_y_1:cut_y_2,:]


            # for i in range(frame.shape[0]):
            #     for j in range(frame.shape[1]):
            #         p1 = (i,j)
            #         if(dist(p1,pt)>120**2 or dist(p1,pt)<12100):
            #             frame[i,j,:]=255
            # lap1 = time.time()-acc
            # print('lap2',lap1)

            frame_gray=cv2.cvtColor(c_cut,cv2.COLOR_BGR2GRAY)
            edgs=cv2.Canny(frame_gray,200,200)
            dst = cv2.goodFeaturesToTrack(edgs, 5, 0.05, 15)
            lap1 = time.time()-acc
            print('lap3',lap1)


            dst = np.int0(dst)
            d_list =[]
            for i in dst:
                x1,y1 =i.ravel()
                pt = (x1,y1)
                d_list.append(pt)


            is_paired =[False] *len(d_list)
            for p1 in d_list:
                for p2 in d_list:
                    if(not (p1 is p2)):
                        if(is_paired[d_list.index(p1)] == False and
                           is_paired[d_list.index(p2)] == False):
                            if(check_point_to_pair(p1,p2)):
                                frame_list.append((p1,p2))
                                is_paired[d_list.index(p1)] = True
                                is_paired[d_list.index(p2)] = True

                                cv2.circle(frame, (p1[0]+dev_x, p1[1]+dev_y), 5, (0,0,255), -1)
                                cv2.circle(frame, (p2[0]+dev_x, p2[1]+dev_y), 5, (0,0,255), -1)


            if(len(frame_list)!=0):
                prepare_list.append(frame_list)
            pair_list = sum(prepare_list,[])

            if(len(prepare_list)<15):

                # print('not enough pairs')
                pass
            else:
                values,m_list= merge_pairs(pair_list)
                # print(m_list)
                # print(values)


                id_best = values.index(max(values))

                best_pair = squash(m_list[id_best])

                for pt in best_pair:
                    cv2.circle(frame, (pt[0]+dev_x,pt[1]+dev_y), 3, (0,255,255), -1)


            if(len(prepare_list)==15):
                prepare_list.pop(0)
            else:
                pass






            for i in dst:
                x1, y1 = i.ravel()
                cv2.circle(frame, (x1, y1), 3, 255, -1)

            if(res[loc]>THRESHHOLD):
                frame = cv2.rectangle(frame, (y,x), (y + cols, x + rows ), (0,255,255), 2)
            else:
                frame = cv2.rectangle(frame, (y,x), (y + cols, x + rows ), (255,0,0), 2)

            lap =time.time()-acc
            print('lap',lap)



            cv2.imshow('lol',c_cut)
            cv2.waitKey(1)



            # _,_,res=find_match(imgSrc)
            # # i,j,small_res=find_small_match(res)
            # print(i,j)


            # cv2.imshow('res',res)
            # cv2.waitKey(200)
