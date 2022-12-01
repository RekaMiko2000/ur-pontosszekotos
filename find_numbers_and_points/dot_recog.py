import cv2 as cv
import numpy as np

def get_points(img):
    img_rgb=img.copy()
    points=[]
    cv.waitKey(0)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    #cv.imshow("Szurke",img_gray)
    template = cv.imread('pictures/pont.png',0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        points.append([pt[0],pt[1],w,h])
    cv.imshow("Contoured dots",img_rgb)
    cv.waitKey(0)
    return points
