import geopandas as gpd
from shapely import Polygon, Point
import copy

def listPoints(someGeometry):

    pointList = []
    try:
        for part in someGeometry:
            x, y = part.exterior.coords.xy
            pointList.append(list(zip(x,y)))
    except:
        try:
            x,y = someGeometry.exterior.coords.xy
            pointList.append(list(zip(x,y)))
        except:
            pointList.append(someGeometry)
    return pointList


def moving_points(points, polygon, pot_size):
    
    new_points = []
    for point in points:
        if Point([(point[0], point[1]-pot_size)]).intersects(polygon).any() != True:
            new_points.append([point[0], point[1]-pot_size])
        elif Point([(point[0], point[1]+pot_size)]).intersects(polygon).any() != True:
            new_points.append([point[0], point[1]+pot_size])
        elif Point([(point[0]-pot_size, point[1])]).intersects(polygon).any() != True:
            new_points.append([point[0]-pot_size, point[1]])
        elif Point([(point[0]+pot_size, point[1])]).intersects(polygon).any() != True:
            new_points.append([point[0]+pot_size, point[1]])

    return new_points


def scaling_points(points, pot_size):

    point_list = gpd.GeoSeries([Point(points[i][0], points[i][1]) for i in range(len(points))])

    buffered_point = point_list.buffer(pot_size, join_style=2)
    merged_point = gpd.GeoSeries(buffered_point[0])
    for i in range(1, len(buffered_point)):
        merged_point = merged_point.union(buffered_point[i])

    point_exploded = merged_point.explode()
    #new = [point_exploded.geometry.apply(lambda x: listPoints(x)).values.tolist()[i][0] for i in range(len(point_exploded))]

    return gpd.GeoSeries(point_exploded[0])


def scaling_obstacles(vertices, robot_size):

    polygon_list = gpd.GeoSeries(Polygon(vertices[i]) for i in range(len(vertices)))

    buffered_polygon = polygon_list.buffer(robot_size, join_style=2)

    merged_polygon = gpd.GeoSeries(buffered_polygon[0])
    for i in range(1, len(buffered_polygon)):
        merged_polygon = merged_polygon.union(buffered_polygon[i])

    polygon_exploded = merged_polygon.explode()
    #new = [polygon_exploded.geometry.apply(lambda x: listPoints(x)).values.tolist()[i][0] for i in range(len(polygon_exploded))]
   
    return gpd.GeoSeries(polygon_exploded[0])


def scaling_map(vertice, points, robot_size, pot_size):
    vertices = copy.deepcopy(vertice)[1:]
    scale1 = scaling_obstacles(vertices, robot_size)
    scale2 = scaling_points(points, pot_size)
    scale3 = scale1
    scale = scale1
    for i in range(len(scale2)):
        scale1 = scale1.union(scale2[i])
        scale3 = scale3.difference(scale2[i])
    for i in range(len(scale3)):
        scale1 = scale1.union(scale3[i])
    polygon_exploded = scale1.explode()
    new = [polygon_exploded.geometry.apply(lambda x: listPoints(x)).values.tolist()[i][0] for i in range(len(polygon_exploded))]

    new_points = moving_points(points, scale, pot_size)
    new.append(vertice[0])
    return new, new_points


mapp=[[[0,5], [2,10], [10,12], [10,7], [10,0], [0,2], [0,5]], [[0,0], [1,1], [-5,0], [-10,-2], [0,0]], [[-10,-10], [-5,-8], [-9,-7], [1,-8], [-10,-10]]]
pp = [[-10,10], [12,-6], [-6,5], [10,0], [1,11]]
scaling_map(mapp,pp,1,2)

