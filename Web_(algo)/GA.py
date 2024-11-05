from random import random, shuffle, sample
from base import *
from path import Path

def sort_path(start_point, points, path):
    del path[-1]
    
    i = points.index(start_point)
    j = path.index(i)
    
    new_path = path[j:] + path[:j]
    return new_path
    
class GA():
    """
        population: величина популяции
        iter: число итераций
        s: коэффициент выборки
        m: коэффициент мутации
    """

    def __init__(self, population, iter, s, m, dis,map, dis_size, start_pos):
        self.population = population
        self.iter = iter
        self.s = s
        self.m = m
        self.dis = dis
        self.map = map
        self.dis_size = dis_size
        self.start_pos = start_pos

    def fitness_sort(self, dm, individuals):
        individuals.sort(key=lambda i: calculate_dist(dm, i))

    def initialization(self, l):
        base = list(range(l))
        individuals = []
        for i in range(self.population):
            shuffle(base)
            individuals.append(base + [base[0]])
        return individuals

    def selection(self, individuals):
        del individuals[int(self.population * self.s) :]

    def crossover(self, individuals):
        childs = []
        w_size = len(individuals[0]) // 2
        for j in range(len(individuals), self.population):
            p1, p2 = sample(individuals, 2)
            childs.append(
                p1[: w_size - 1]
                + [i for i in p2[:-1] if i not in p1[: w_size - 1]]
                + [p1[0]]
            )
        individuals += childs

    def mutation(self, individuals):
        sampling = list(range(1, len(individuals[0]) - 1))
        for item in individuals:
            if random() < self.m:
                i, j = sample(sampling, 2)
                item[i], item[j] = item[j], item[i]

    def run(self, points):
        dx, dy = normalize(self.dis, self.map)
        dis_points = move_odom(points, dx, dy, self.dis_size)
        dis_points = np.array(dis_points)
        dis_points = list(dis_points.astype(int))

        l = len(dis_points)
        dm = distance_matrix(self.dis,dis_points)
        individuals = self.initialization(l)
        for i in range(self.iter):
            self.fitness_sort(dm, individuals)
            self.selection(individuals)
            self.crossover(individuals)
            self.mutation(individuals)
        self.fitness_sort(dm, individuals)
        
        
        new_path = sort_path(self.start_pos, points, individuals[0])
        d = []
        for i in range(len(dis_points)):
            d.append(dis_points[new_path[i]])
        d = np.array(d)
        return Path(indx=new_path, leng=calculate_dist(dm, new_path), path = Path_maker(self.dis, d))

