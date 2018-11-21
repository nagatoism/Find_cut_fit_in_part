import cv2
from glob import *

def get_patch(img,p1,p2):
    patch=img[p1[1]:p2[1],p1[0]:p2[0],:]
    return patch
def get_center_patch(img):
    DIS=7*45
    centx=img.shape[1]//2
    centy=img.shape[0]//2
    x1 = max(0,centx-DIS)
    y1 = max(0,centy-DIS)
    x2 = min(img.shape[1],centx+DIS)
    y2 = min(img.shape[0],centy+DIS)

    patch=get_patch(img,(x1,y1),(x2,y2))

    return patch

if __name__=='__main__':
    f_list = glob('./TTQIMG/1/Img6/*')
    img = cv2.imread(f_list[0])
    img = cv2.resize(img,(img.shape[1]//2,img.shape[0]//2))
    cv2.imshow('lol',img)
    cv2.waitKey(1000)
    patch =get_patch(img,(297,161),(497,365))
    cv2.imshow('lol',patch)
    cv2.waitKey(1000)

    cv2.imwrite('./TTQIMG/test_cut6.png',patch)
