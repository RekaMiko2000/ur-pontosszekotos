import math

def return_points_coords(numbers_coords,points_coords):
    points_for_numbers={}
    for num in numbers_coords:
        min=get_difference(numbers_coords[num],[points_coords[0][0],points_coords[0][1]])
        min_point=points_coords[0]
        for i in range(len(points_coords)):
            difference=get_difference(numbers_coords[num],[points_coords[i][0],points_coords[i][1]])
            if difference<min:
                min=difference
                min_point=points_coords[i]
        points_for_numbers[num]=min_point
        points_coords.remove(min_point)
    return points_for_numbers

def get_difference(point_one,point_two):
    diff_x=pow(point_two[0]-point_one[0],2)
    diff_y=pow(point_two[1]-point_one[1],2)
    difference=math.sqrt(diff_x+diff_y)
    return difference