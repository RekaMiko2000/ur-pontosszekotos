import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import re
import pprint

def search_for_all(file_names,img):
    numbers={}
    img_rgb=img.copy()
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    used_vals=[]
    for file_name in file_names:
        if isinstance(file_names[file_name],str) and file_names[file_name]!="":
            #print(file_name)
            template = cv.imread(file_names[file_name],0)
            w, h = template.shape[::-1]
            res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
            _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(res, None)
            matchLoc = maxLoc
            #print(_maxVal)
            if matchLoc not in used_vals:
                if _maxVal>0.7:
                    used_vals.append(matchLoc)
                    numbers[file_name]=matchLoc
                cv.rectangle(img_rgb, matchLoc, (matchLoc[0] + w, matchLoc[1] + h), (0,0,0), 2)
                cv.rectangle(res, matchLoc, (matchLoc[0] + w, matchLoc[1] + h), (0,0,0), 2)
            #cv.imshow("result",img_rgb)
            #cv.waitKey(0)
        else:
            continue
    cv.imshow("result",img_rgb)
    cv.waitKey(0)
    return numbers

def assign_num_to_pic(template_num):
    numbers_path={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None, 10:None, 11:None, 12:None, 13:None, 14:None, 15:None, 16:None}
    for i in range(len(numbers_path)+1):
        picture_path=""
        if os.path.isfile(f'pictures/template_{str(template_num)}/{str(i)}.png'):
            picture_path=f'pictures/template_{str(template_num)}/{str(i)}.png'
        elif os.path.isfile(f'pictures/template_{str(template_num)}/{str(i)}.jpg'):
            picture_path=f'pictures/template_{str(template_num)}/{str(i)}.jpg'
        elif os.path.isfile(f'pictures/template_{str(template_num)}/{str(i)}.jpeg'):
            picture_path=f'pictures/template_{str(template_num)}/{str(i)}.jpeg'
        else:
            continue
        numbers_path[i]=picture_path
    return numbers_path

if __name__=="__main__":
    numbers_path=assign_num_to_pic()
    numbers=search_for_all(numbers_path)
