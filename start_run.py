import argparse
import sys
import socket
import os
import pprint
import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
number_and_point_recog_path = dir_path + os.sep + "find_numbers_and_points"
sys.path.append(number_and_point_recog_path)

import contour_points
import draw
import convert_to_robot_coords
import write_to_file
import dot_recog
import number_recog
import get_closest_points

def create_args():
    parser=argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '-file',
        '--file',
        type=str,
        help="The path for the picture we run the script on"
    )
    return parser

if __name__=="__main__":
    tcp_client=draw.TCP_Client("10.150.1.1",30002)
    socket=tcp_client.socket
    parser=create_args()
    args=parser.parse_args()
    filename='pictures/napocska.jpg'
    if args.file:
        filename=args.file
    img_rgb = cv2.imread(filename)
    scale_percent=120
    width = int(img_rgb.shape[1] * (scale_percent / 100))
    height = int(img_rgb.shape[0] * (scale_percent / 100))
    resized = cv2.resize(img_rgb, (width,height), interpolation = cv2.INTER_AREA)
    points=dot_recog.get_points(resized)
    numbers_path=number_recog.assign_num_to_pic(2)
    numbers=number_recog.search_for_all(numbers_path,resized)
    points_closest=get_closest_points.return_points_coords(numbers,points)
    #contour_points.contour_points(resized,points_closest)
    center_coords_mm={}
    for key in points_closest:
        center_coords_mm[key]=[
            (points_closest[key][0]+(points_closest[key][2]/2))*0.264583,
            (points_closest[key][1]+(points_closest[key][3]/2))*0.264583
        ]
    #pprint.pprint(center_coords_mm)
    robot_coords=convert_to_robot_coords.return_distances(center_coords_mm)
    pprint.pprint(robot_coords)
    filename=filename.replace("pictures/","")
    filename=filename.replace(".jpg","")
    filename=filename.replace(".jpeg","")
    filename=filename.replace(".png","")
    filename_for_coords=f"coordinates_for_dots-{filename}.txt"
    write_to_file.write_to_file(robot_coords, filename_for_coords)
    print(filename_for_coords)
    #socket.draw(filename_for_coords)
    