import numpy as np
import math

previous_health = 0
previous_damage = 0      # finding the edge of the thresh image

def calculate(edges):
    ''' Calculating the damage by measuring the difference is length 
            of the total health bar and health bar after damage
            (remaing_health)'''

    # variable to keep track of previous remaing health
    global previous_health
    sum_of_white_pixel = 0

    # Total health bar width in numpy array (a)
    Total_health = len(edges)
    # Total health bar height in numpy array (b)
    Total_vertical_pixel = len(edges)
    Total_horizontal_pixel = edges.shape[1] 
    # loop through all the (a) rows
    '''
	   b
	   ^
	   |
	   0000000000000000002550000000  <- a
	   0000000000000000002550000000  <- a
	   0000000000000000002550000000  <- a
	   0000000000000000002550000000  <- a
	   0000000000000000002550000000  <- a'''

    correctEdge = False
    for edge in edges:
        # detecting the white pixels(255) by eliminating the nonzero indices
        white_pixel = np.nonzero(edge)[0]
        no_pixel_in_one_row = len(white_pixel)
        if no_pixel_in_one_row < 1:
            continue
        else:
            if (white_pixel[0] - white_pixel[-1]) <= 4:
                correctEdge = True
            else:
                continue
        # if the multiple lines arises take the average of each (a) row
        avg_of_white_pixel = sum(white_pixel)/len(white_pixel)

        # if the image obtained has no edge set the average to 0
        if math.isnan(avg_of_white_pixel):
            avg_of_white_pixel = 0

        # taking sum of all white pixel in the (a) rows
        sum_of_white_pixel += int(avg_of_white_pixel)

    if(correctEdge):
        # remaing health is calculate by taking the average of white pixels vertical (b colums)
        remaing_health = int(sum_of_white_pixel/Total_vertical_pixel)
        remaing_health_percentage = remaing_health/Total_horizontal_pixel * 100
        print(remaing_health_percentage)
        return(int(remaing_health_percentage))
