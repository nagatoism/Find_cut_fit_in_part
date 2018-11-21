import cv2


video=cv2.VideoCapture(0)
frame_width = int(video.get(3))
frame_height = int(video.get(4))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width//2,frame_height//2))
idx = 0
while(video.isOpened()):
    idx+=1
    ret,frame=video.read()
    video.set(cv2.CAP_PROP_FOCUS, 20)

    frame = cv2.resize(frame,(frame.shape[1]//2,frame.shape[0]//2))
    out.write(frame)
    cv2.imshow('lol',frame)
    cv2.waitKey(1000//25)

    if(idx==150):
        cap.release()
        out.release()
        break
