import math
import numpy as np
from matplotlib.patches import Rectangle
from rdp import rdp
from skimage import morphology
from numba import njit, jit
import sys

import numpy as np
from matplotlib.collections import LineCollection
from rdp import rdp
from numba.typed import List

@njit
def euc(dot1, dot2):
    return ((dot1[0]-dot2[0])**2 + ((dot1[1]-dot2[1])**2))**0.5

@njit
def liang_barsky(x_min, y_min, x_max, y_max, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
    t_enter = 0.0
    t_exit = 1.0

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return False
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                if t > t_enter:
                    t_enter = t
            else:
                if t < t_exit:
                    t_exit = t

    if t_enter > t_exit:
        return False

    x1_clip = x1 + t_enter * dx
    y1_clip = y1 + t_enter * dy
    x2_clip = x1 + t_exit * dx
    y2_clip = y1 + t_exit * dy

    return True
    
def cut(discrete):
    temp = []
    for line in discrete:
        if line.any():
            temp.append(line)
    temp = np.array(temp).T
    temp2 = []
    for line in temp:
        if line.any():
            temp2.append(line)
    temp2 = np.array(temp2).T
    return temp2

@njit
def grid_maker(obstacles ,num1, num2, min_x, min_y, d_size):
    grid = []
    for j in range(num2):
        for i in range(num1):
            f = [min_x - 1 + i * d_size, min_y - 1 + j * d_size, min_x - 1 + i * d_size + d_size,
                        min_y - 1 + j * d_size + d_size]
            grid.append(f)
            
    discrete_num = []
    sep = 0
    for i in range(len(grid)):
        f = grid[i]
        x_min, y_min = f[0], f[1]
        x_max, y_max = f[2], f[3]
        for j in range(len(obstacles)):
            obst = obstacles[j]
            for k in range(len(obst)-1):
                point1 = obst[k]
                point2 = obst[k+1]
                x1, y1 = point1[0], point1[1]
                x2, y2 = point2[0], point2[1]
                clipped_line = False
                
                if liang_barsky(x_min, y_min, x_max, y_max, x1, y1, x2, y2):  
                    clipped_line = True
                if clipped_line:
                    sep = 1
                    break

        if sep == 1:
            discrete_num.append(1)
        else:
            discrete_num.append(0)
        sep = 0
    return grid, discrete_num

@njit
def sad(lidars):
    lidar = []
    for elem in lidars:
        for entry in elem:
            lidar.append(entry)
    points_approximate = []
    ki = 0
    kj = 0
    while ki < len(lidar):
        points_sum = []
        while kj < len(lidar):
            if kj != ki:
                # print(kj, ki, len(lidars))
                p = lidar[ki]
                pp = lidar[kj]
                #print(p[0])
                if np.sqrt((p[0] - pp[0])*(p[0] - pp[0]) + (p[1] - pp[1])*(p[1] - pp[1])) < 0.02:
                    points_sum.append(pp)
                    del lidar[kj]
            kj += 1
        kj = 0
        ki += 1
        if len(points_sum) > 0:
            av_x = 0
            av_y = 0
            for k in range(len(points_sum)):
                c = points_sum[k]
                av_x += c[0]
                av_y += c[1]
            points_approximate.append((av_x / len(points_sum), av_y / len(points_sum)))
    return points_approximate

class NNA:
    def __init__(self, real_map, discrete_size):
        sys.setrecursionlimit(20000)
        self.map = real_map
        self.discrete_size = discrete_size

    def prepareMap(self):

        minx = self.map[0][0][0]
        miny = self.map[0][0][1]
        maxx = self.map[0][0][0]
        maxy = self.map[0][0][1]

        min_x, min_y, max_x, max_y = self.set_window_size(self.map, minx, miny, maxx, maxy)
        
        grid, discrete_num, num1, num2 = self.discrete(self.map, self.discrete_size, min_x, min_y, max_x, max_y)
        #print(discrete_num)
        #print(grid)
        new = np.array(discrete_num)
        #print(new)
        new = np.reshape(new, (num1, num2))
        #new = np.rot90(new,2)
        
        new = morphology.binary_dilation(new)
        new = morphology.binary_dilation(new)
        #new = morphology.binary_dilation(new)
        new = new.astype(int)
        #new = new[:5, :]
        #new2 = cut(new)
        
        return new

    def discrete(self, lidar, d_size, min_x, min_y, max_x, max_y):

        num1 = round((abs(max_x) + abs(min_x) + 2) / d_size)
        num2 = round((abs(max_y) + abs(min_y) + 2) / d_size)

        while num1 * d_size + min_x - 1 > max_x + 1:
            num1 -= 1

        while num2 * d_size + min_y - 1 > max_y + 1:
            num2 -= 1

        #print(num1)
        lidar_temp = List(List(x) for x in lidar)
        #print(lidar_temp[0][0])
        grid, dis = grid_maker(lidar_temp, num1, num2, min_x, min_y, d_size)

        #print(grid)
        return grid, dis, num1, num2

    def set_window_size(self, lid, min_x, min_y, max_x, max_y):
        min_value_x = min_x
        min_value_y = min_y
        max_value_x = max_x
        max_value_y = max_y
        for i in range(len(lid)):
            for j in range(len(lid[i])):
                if lid[i][j][0] < min_value_x:
                    min_value_x = lid[i][j][0]
                if lid[i][j][1] < min_value_y:
                    min_value_y = lid[i][j][1]
                if lid[i][j][0] > max_value_x:
                    max_value_x = lid[i][j][0]
                if lid[i][j][1] > max_value_y:
                    max_value_y = lid[i][j][1]

        return min_value_x, min_value_y, max_value_x, max_value_y

