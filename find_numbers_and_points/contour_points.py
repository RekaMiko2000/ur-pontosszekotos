#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

def contour_points(img_rgb,dict_of_nums_and_coords):
    im=img_rgb.copy()
    for x in dict_of_nums_and_coords:
        x,y,w,h,=dict_of_nums_and_coords[x]
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('im', im)
    cv2.waitKey(0)

