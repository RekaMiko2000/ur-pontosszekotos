import pprint
import numpy as np

def return_distances(coords_mm):
    robot_coords={}
    #x_from=740.5
    #y_from=356.0
    x_from_mm=195.9237 # 159/196=0.816
    y_from_mm=94.1915 # 94/-235=-0.4
    for key in coords_mm:
        x=coords_mm[key][0]
        y=coords_mm[key][1]
        if x_from_mm>x:
            diff_x=(-1.6)*(x_from_mm-x)
        elif x_from_mm<x:
            diff_x=(-1.65)*(x_from_mm-x)
        else:
            diff_x=(-1)*(x_from_mm-x)
        diff_y=(1.65)*(y_from_mm-y)
        robot_coords[key]=[round((0.816*x_from_mm-diff_x)*0.001,5),round((y_from_mm/(-0.4)-diff_y)*0.001,5)]
    return robot_coords