import numpy as np

class Astar:
    def gen_one_links_8grid(self, map, x, y):  # функция получения связей для определенной дискреты
        temp = []
        for y_sub in range(max(y - 1, 0), min(y + 2, map.shape[
            0])):  # исследуем вершины в радиусе 1, не зыбваем, что карта у нас не зациклена как в пакмане
            for x_sub in range(max(x - 1, 0), min(x + 2, map.shape[1])):
                if map[y_sub, x_sub] != 1 and ((y_sub == y and x_sub == x) != 1):  # если вершина не препятствие и не начальная вершина, то добавляем связь в массив для словаря
                    temp.append((y_sub, x_sub))
        return np.array(temp)


    def link_8grid(self, map):  # функция создания графа 8grid
        links = {}  # используем словарь как наиболее удобный формат хранения связей
        for y in range(map.shape[0]):  # проходимся по всей карте
            for x in range(map.shape[1]):
                if map[y, x] != 1:  # если дискрета не 1, получаем для нее связи, иначе считаем, что связей нет
                    links[y, x] = self.gen_one_links_8grid(map, x, y)
                else:
                    links[y, x] = 0
        return links


    def gen_one_links_4grid(self, map, x, y):  # функция получения связей для определенной дискреты
        temp = []
        for y_sub in range(max(y - 1, 0), min(y + 2, map.shape[
            0])):  # исследуем вершины в радиусе 1, не зыбваем, что карта у нас не зациклена как в пакмане
            for x_sub in range(max(x - 1, 0), min(x + 2, map.shape[1])):
                if abs(y_sub - y) + abs(x_sub - x) != 1:
                    continue
                if map[
                    y_sub, x_sub] != 1:  # если вершина не препятствие и не начальная вершина, то добавляем связь в массив для словаря
                    temp.append((y_sub, x_sub))
        return np.array(temp)


    def link_4grid(self, map):  # функция создания графа 8grid
        links = {}  # используем словарь как наиболее удобный формат хранения связей
        for y in range(map.shape[0]):  # проходимся по всей карте
            for x in range(map.shape[1]):
                if map[y, x] != 1:  # если дискрета не 1, получаем для нее связи, иначе считаем, что связей нет
                    links[y, x] = self.gen_one_links_4grid(map, x, y)
                else:
                    links[y, x] = 0
        return links


    def Heuristics(self, start, target, type_h):
        if type_h == 0:
            return (abs(start[0] - target[0]) + abs(start[1] - target[1]))
        elif type_h == 1:
            dx = abs(start[1] - target[1])
            dy = abs(start[0] - target[0])
            return (dx + dy + (1.414 - 2) * min(dx, dy))
        elif type_h == 2:
            return ((start[1] - target[1]) ** 2 + (start[0] - target[0]) ** 2) ** 0.5


    def Astar(self,links,target,type_h,open_array,closs_array,weight_array_q,weight_array_h):
        sorted_open_array = sorted(open_array.items(), key=lambda x: x[1])
        first_links = sorted_open_array[0][0]
        for link in links[first_links[0],first_links[1]]:
            q = int(((abs(first_links[0] - link[0]) + abs(first_links[1] - link[1])))**0.5 * 10)
            if weight_array_q[link[0],link[1]] > weight_array_q[first_links[0],first_links[1]] + q: #если полученный путь к вершине меньше ранее найденного пути, то перезпишем расстояние найденное в данный момент
                weight_array_q[link[0],link[1]] = weight_array_q[first_links[0],first_links[1]] + q
            h = self.Heuristics(link,target,type_h)
            weight_array_h[link[0],link[1]] = h
            if (tuple(link) in closs_array) != 1:
                open_array[link[0],link[1]] = weight_array_q[link[0],link[1]] + weight_array_h[link[0],link[1]]
        del open_array[first_links]
        closs_array.append(first_links)
        #print(closs_array)
        if list(first_links) == target:
            
            return 
        self.Astar(links,target,type_h,open_array,closs_array,weight_array_q,weight_array_h)


    def Astar_get_path(self, links, closs_array, start_pos):
        next_pos = closs_array[-1]
        path = [next_pos]
        while list(path[-1]) != start_pos:
            #print(path)
            for link in links[next_pos[0], next_pos[1]]:
                if tuple(link) in closs_array:
                    next_pos = link
                    path.append(next_pos)
                    break
        return np.array(path)
    
    def Dijkstra3_et(self,weight_array,links,end_pos,path):

        for link in links[end_pos[0],end_pos[1]]:#ищем путь от целевой точки к начальной, проверяя все возможные переходы от последней найденной правильной вершины
            temp = int(((abs(end_pos[0] - link[0]) + abs(end_pos[1] - link[1]))**0.5)*10)#считаем расстояние до следующий вершины
            if weight_array[link[0],link[1]] == weight_array[end_pos[0],end_pos[1]] - temp:#если мы нашли искомый преход, то запоминаем его и исследуем вершину в которую переши
                path.append(link)
                if weight_array[link[0],link[1]] != 0:#если наш переход не начальная точка с 0 весом, то исследуем вершину
                    self.Dijkstra3_et(weight_array,links,link,path)
                return
        print("Путь до данной точки не найден")
        return


    def Astar_all(self, map, start_pos, target, type_h):
        weight_array_q = np.ones((map.shape[0],map.shape[1]))#создаем матрицу весов вершин графа
        weight_array_q *= 999#в начальный момент считаем, что переходить с одной вершины на другой максимально дорого
        weight_array_q[start_pos[0],start_pos[1]] = 0
        weight_array_h = np.ones((map.shape[0],map.shape[1]))#создаем матрицу весов вершин графа
        weight_array_h *= 999 #в начальный момент считаем, что переходить с одной вершины на другой максимально дорого
        weight_array_h[start_pos[0],start_pos[1]] = self.Heuristics(start_pos,target,type_h)
        open_array = {}
        open_array[start_pos[0],start_pos[1]] = self.Heuristics(start_pos,target,type_h)
        closs_array = []
        if type_h != 0:
            links = self.link_8grid(map) 
        else:
            links = self.link_4grid(map) 
        #print(links)
        self.Astar(links,target,type_h,open_array,closs_array,weight_array_q,weight_array_h)
        weight_array_h = np.array(weight_array_h, dtype='i')
        weight_array_q = np.array(weight_array_q, dtype='i')
        path = []
        path.append(target)
        self.Dijkstra3_et(weight_array_q,links,target,path)
        path = np.array(path)
        #print(path)
        return path


    def print_path(self, ax, start_pos, end_pos, path):
        
        ax.plot(start_pos[1], start_pos[0], 'ro')
        ax.plot(end_pos[1], end_pos[0], 'go')
        ax.plot(path[0:path.shape[0], 1], path[0:path.shape[0], 0],'b')
        


    def paint_borders(self, map):
        map[0, 0:map.shape[1]] = 1
        map[0:map.shape[0], 0] = 1
        map[map.shape[0] - 1, 0:map.shape[1]] = 1
        map[0:map.shape[0], map.shape[1] - 1] = 1