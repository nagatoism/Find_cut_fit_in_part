import os
import shutil
import glob
import glob
import numpy as np
import cv2
def get_imgs(path):
    files = []
    if(path[-1:]!='/'):
        path+='/'
    f_list = glob.glob(path+'*')
    for i in f_list:
        files.append(cv2.imread(i))

    files = np.asarray(files)
    return files
if __name__ == '__main__':
    files = get_imgs('./yellow')
    print(files.shape)
    print(files[0].shape)
