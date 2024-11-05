from GA import GA
import nearest_neighbor
import base
from rdp import rdp

def scale(m):
    for i in range(len(m)):
        for k in range(len(m[i])):
            #print(m[i][k][0])
            m[i][k] = (int(m[i][k][0]*100), int(m[i][k][1]*100))
    return m


def main(map, points, start_pos):
    map.append([[0,3],[3,3],[3,0],[0,0],[0,3]])
    map = scale(map)
    points=[[int(point[0]*100),int(point[1]*100)] for point in points]
    start_pos= [int(start_pos[0]*100), int(start_pos[1]*100)]
    dis_s = 5
    g = nearest_neighbor.NNA(map, dis_s)
    dis = g.prepareMap()
    paths = []

    ga = GA(1500, 40, 0.2, 0.5, dis, map, dis_s, start_pos)
    paths.append(ga.run(points))

    plot = paths[0].path

    plot= [(x,y) for y,x in plot]
    dx, dy = base.normalize(dis, map)
    pl = base.move_discrete(plot, dx, dy, dis_s)
    pll = rdp(pl)
    pll = [(int(x+3),int(y+2)) for x,y in pll]
    return pll