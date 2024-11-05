from math import sqrt
import numpy as np
from AstarF import Astar
from nearest_neighbor import liang_barsky
from time import time

def normalize_real(array):
    best_min_x = 100000
    best_min_y = 100000
    for elem in array:
        min_elem_x = min([x for x,_ in elem])
        max_elem_y = min([y for _,y in elem])
        if min_elem_x < best_min_x:
            best_min_x = min_elem_x
        if max_elem_y < best_min_y:
            best_min_y = max_elem_y
    return best_min_x, best_min_y

def normalize_discr(discr):
    best_min_x = -100000
    best_max_y = 100000
    for y in range (discr.shape[0]):
        for x in range (discr.shape[1]):
            if discr[y, x] == 1:
                best_min_x = x
                best_max_y = y
                return best_min_x, best_max_y

def normalize(discr, real):
    rx,ry = normalize_real(real)
    disx, disy =  normalize_discr(discr)
    dx,dy = disx*0.3 - rx, disy*0.3 - ry
    return dx, dy

def move_odom(odom, thrx, thry, dis):
    return_arr = [(elem[0]+(thrx), (elem[1]+thry)*1) for elem in odom]
    return_arr = np.array(return_arr)*1/dis
    return return_arr

def move_discrete(path, thrx, thry, dis):
    return_arr = np.array(path)/(1/dis)
    #return_arr = return_arr.astype(float)
    #return_arr /= 1/dis
    return_arr = [((elem[0]-thrx)*1, (elem[1]-thry)*1) for elem in return_arr]
    return return_arr

def euclidean_dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def Astar_dist(dis, a, b):
    path = Astar().Astar_all(dis, a, b, 2)
    #Astar().print_path(dis, start_pos, end_pos, path)
    return(len(path))

def dist(dis,a,b):
    if a[0]!= b[0] and a[1]!=b[1]:
        print(list(a))
        return Astar_dist(dis, list(a)[::-1], list(b)[::-1])#+euclidean_dist(a, b)
    else:
        return euclidean_dist(a, b)

def Path_maker(dis, points):

    path = Astar().Astar_all(dis, list(points[0])[::-1], list(points[1])[::-1],2)
    path = list(path)[::-1]
    for i in range(1, len(points)-1):
        path_one = Astar().Astar_all(dis, list(points[i])[::-1], list(points[i+1])[::-1], 2)
        path_one = list(path_one)[::-1]
        path.extend(path_one)
    path_one = Astar().Astar_all(dis, list(points[-1])[::-1], list(points[0])[::-1], 2)
    path_one = list(path_one)[::-1]
    path.extend(path_one)

    p = list(points)
    p.append(p[0])
    robot_x = [x for x,_ in p]
    robot_y = [y for _,y in p]

    return path

def calculate_dist(dm, indx):
    dist = 0
    for i in range(len(indx) - 1):
        dist += dm[indx[i]][indx[i + 1]]
    return dist

def distance_matrix(dis, points):
    return [[dist(dis, a, b) for b in points] for a in points]
