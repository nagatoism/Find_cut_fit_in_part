import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import os
from glob import *



from get_patch import get_patch,get_center_patch
from algo import *


if __name__ == '__main__':

    img = cv2.imread('./TTQIMG/test_cut6.png', cv2.IMREAD_COLOR)
    # img = cv2.resize(img, (img.shape[1]//2,img.shape[0]//2))
    # cv2.imshow('lat',img)
    # cv2.waitKey(5000)
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # cv2.imshow('lat',small_img)
    # cv2.waitKey(5000)

    rows, cols, _ = img.shape



    # his_s_patch = ColarHist(small_img)



    # imgSrc=cv2.imread('p3.jpg')
    #
    # _,_,res=find_match(imgSrc)
    # small_res=find_math(res)
    KERNEL=np.ones((3,3),np.uint8)
    THRESHHOLD=0.65

    idx = 0
    pair_list =[]
    prepare_list =[]
    file_list = glob('./TTQIMG/1/Img6/*')



    for f in file_list:

        acc = time.time()
        idx+=1
        frame = cv2.imread(f)

        frame_list = []


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

            cut_x_1 = max(0,pt[0]-130)
            cut_x_2 = min(pt[0]+130,frame.shape[0])
            cut_y_1 = max(0,pt[1]-130)
            cut_y_2 = min(pt[1]+130,frame.shape[1])
            dev_x = pt[0]-130
            dev_y = pt[1]-130

            c_cut =frame[cut_x_1:cut_x_2,cut_y_1:cut_y_2,:]
            c_cut =c_cut.copy()

            pt2 =(130,130)

            for i in range(c_cut.shape[0]):
                for j in range(c_cut.shape[1]):
                    p1 = (i,j)
                    if(dist(p1,pt2)>12000 or dist(p1,pt2)<10000):
                        c_cut[i,j,:]=255
            lap1 = time.time()-acc
            print('lap2',lap1)

            frame_gray=cv2.cvtColor(c_cut,cv2.COLOR_BGR2GRAY)
            edgs=cv2.Canny(frame_gray,200,200)
            # cv2.imshow('lol',edgs)
            # cv2.waitKey(2000)
            dst = cv2.goodFeaturesToTrack(edgs, 5, 0.05, 15)
            lap1 = time.time()-acc
            print('lap3',lap1)


            dst = np.int0(dst)
            d_list =[]
            for i in dst:
                x1,y1 =i.ravel()
                pt = (x1,y1)
                d_list.append(pt)


            # is_paired =[False] *len(d_list)
            # for p1 in d_list:
            #     for p2 in d_list:
            #         if(not (p1 is p2)):
            #             if(is_paired[d_list.index(p1)] == False and
            #                is_paired[d_list.index(p2)] == False):
            #                 if(check_point_to_pair(p1,p2)):
            #                     frame_list.append((p1,p2))
            #                     is_paired[d_list.index(p1)] = True
            #                     is_paired[d_list.index(p2)] = True
            #
            #                     cv2.circle(frame, (p1[0]+dev_x, p1[1]+dev_y), 5, (0,0,255), -1)
            #                     cv2.circle(frame, (p2[0]+dev_x, p2[1]+dev_y), 5, (0,0,255), -1)
            #
            #
            # if(len(frame_list)!=0):
            #     prepare_list.append(frame_list)
            # pair_list = sum(prepare_list,[])
            #
            # if(len(prepare_list)<15):
            #
            #     # print('not enough pairs')
            #     pass
            # else:
            #     values,m_list= merge_pairs(pair_list)
            #     # print(m_list)
            #     # print(values)
            #
            #
            #     id_best = values.index(max(values))
            #
            #     best_pair = squash(m_list[id_best])
            #
            #     for pt in best_pair:
            #         cv2.circle(frame, (pt[0]+dev_x,pt[1]+dev_y), 3, (0,255,255), -1)
            #
            #
            # if(len(prepare_list)==15):
            #     prepare_list.pop(0)
            # else:
            #     pass






            for i in dst:
                x1, y1 = i.ravel()
                cv2.circle(frame, (x1+dev_x, y1+dev_y), 3, 255, -1)
                cv2.circle(c_cut,(x1,y1),3,255,-1)

            if(res[loc]>THRESHHOLD):
                frame = cv2.rectangle(frame, (y,x), (y + cols, x + rows ), (0,255,255), 2)
            else:
                frame = cv2.rectangle(frame, (y,x), (y + cols, x + rows ), (255,0,0), 2)

            lap =time.time()-acc
            print('lap',lap)



            cv2.imshow('lol',c_cut)
            cv2.waitKey(2000)



            # _,_,res=find_match(imgSrc)
            # # i,j,small_res=find_small_match(res)
            # print(i,j)


            # cv2.imshow('res',res)
            # cv2.waitKey(200)
