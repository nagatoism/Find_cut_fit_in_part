import cv2

video=cv2.VideoCapture('./v4.mp4')
i=0
while(video.isOpened()):
    i+=1

    ret,frame=video.read()
    if(ret==False):
        break
    else:
        pass
    if(i%20==0):

            cv2.imwrite('./yellow/'+str(i)+'.png',frame)
