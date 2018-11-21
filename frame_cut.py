import cv2
import time


video = cv2.VideoCapture(0)
idx = 0
print(video.get((cv2.CAP_PROP_FPS)))
while(video.isOpened()):
    idx+=1



    ret,frame=video.read()
    if(idx==1):
        cv2.imwrite('./svm/cut34.png',frame)
    if(idx%30==1):
        print(frame.shape)
        frame=cv2.resize(frame,(frame.shape[1]//3,frame.shape[0]//3))

        cv2.imshow('lol',frame)
        cv2.waitKey(300)
        print(idx)
        print(frame.shape)



    if(ret==False):
        print(idx)
        break
    else:
        pass
