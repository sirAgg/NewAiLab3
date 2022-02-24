import numpy
#import demo, nmath
import time
import math

neighbours = [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]

board_w = 0
board_h = 0

class Path:
    def __init__(self, start_pos, goal_pos):
        self.points = []
        self.start_pos = start_pos
        self.goal_pos  = goal_pos
        self.is_done = False

def is_at(current_pos, goal_pos):
    return abs(current_pos[0] - goal_pos[0]) < 0.1 and abs(current_pos[1] - goal_pos[1]) < 0.1

class AStar:
    class ANode:
        def __init__(self, f_value, parent):
            self.f_value = f_value
            self.parent_pos = parent

    
    def manhattan_dist(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def euclidean_dist(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def diagonal_dist(a, b):
        return max(abs(a[0] - b[0]),abs(a[1] - b[1]))


    def start(self, path, game_map):
        self.open = []
        self.closed = []
        self.open.append(path.start_pos)
        self.f_values = numpy.zeros((game_map.width, game_map.height), dtype=numpy.float)
        self.f_values[int(path.start_pos[0])][int(path.start_pos[1])] = AStar.diagonal_dist(game_map.goal_pos, path.start_pos)
        self.g_values = numpy.zeros((game_map.width, game_map.height), dtype=numpy.float)
        self.parents = numpy.zeros((game_map.width, game_map.height), dtype=numpy.dtype((numpy.int,2)))
        self.parents[int(path.start_pos[0])][int(path.start_pos[1])] = (-1,-1)
        self.iteration = 0

    def step(self, path, game_map):
        self.iteration += 1
        print(self.iteration)
        current_pos = self.open.pop(0)

        if is_at(current_pos, path.goal_pos):
            reverse_path = []
            pos = list((int(current_pos[0]),int(current_pos[1])))

            while pos[0] > 0:
                reverse_path.append(nmath.Float2(pos[0], pos[1]))
                pos = self.parents[pos[0]][pos[1]]

            path.points = reverse_path
            path.points.reverse()
            return True


        current_g_value = self.g_values[int(current_pos[0])][int(current_pos[1])]
        #neighbours = game_map.get_neighbours(int(current_pos[0]), int(current_pos[1]))


        for n in neighbours:
            if not game_map.check_neighbour(int(current_pos[0]), int(current_pos[1]), n[0], n[1]):
                continue
            p = (current_pos[0] + n[0], current_pos[1] + n[1])
            
            #p = current_pos + n
            prev_f_value = self.f_values[int(p[0])][int(p[1])]
            prev_g_value = self.g_values[int(p[0])][int(p[1])]

            if n[0] == 0 or n[1] == 0:
            #if n[0] == 0 or n[1] == 0:
                g_value = 1
            else:
                g_value = 1.4

            tiletype = map.TileTypes.type(game_map.get(int(p[0]), int(p[1])))

            if tiletype == map.TileTypes.type(map.TileTypes.TREE):
                g_value *= 1.5
            elif tiletype == map.TileTypes.type(map.TileTypes.QUAGMIRE):
                g_value *= 2

            g_value += current_g_value

            h_value = AStar.diagonal_dist(path.goal_pos, p)
            f_value = g_value + h_value

            if prev_g_value <= 0 or prev_g_value > g_value:
                self.f_values[int(p[0])][int(p[1])] = f_value
                self.g_values[int(p[0])][int(p[1])] = g_value
                if prev_g_value <= 0:
                    self.parents[int(p[0])][int(p[1])] = (int(current_pos[0]), int(current_pos[1]))
                    self.open.append(p)

        self.closed.append(current_pos)

        self.open.sort(key= lambda e : self.f_values[int(e[0])][int(e[1])])

        return False


    def __repr__(self):
        return "A*"


#    def visualize(self, path):
#        shape = self.f_values.shape
#
#        max_f = self.f_values[0][0]
#        for x in range(shape[0]):
#            for y in range(shape[1]):
#                if self.f_values[x][y] > max_f:
#                    max_f = self.f_values[x][y]
#
#        
#        for o in self.closed:
#            parent = self.parents[int(o[0])][int(o[1])]
#            demo.DrawLine(nmath.Point(o[0], 0.1, o[1]), nmath.Point(parent[0], 0.1, parent[1]), 4.0, nmath.Vec4(1,1,0,1))
#        
#        for o in self.open:
#            parent = self.parents[int(o[0])][int(o[1])]
#            demo.DrawLine(nmath.Point(o[0], 0.1, o[1]), nmath.Point(parent[0], 0.1, parent[1]), 4.0, nmath.Vec4(1,1,0,1))
#
#
#        for o in self.closed:
#            demo.DrawDot(nmath.Point(o[0],0.1,o[1]), 10, nmath.Vec4(0,0,1,1))
#            
#        for o in self.open:
#            f = self.f_values[int(o[0])][int(o[1])]
#            demo.DrawDot(nmath.Point(o[0],0.1,o[1]), 10, nmath.Vec4(0,f/max_f,0,1))
#            
#
#        prev_p = path.start_pos
#        for p in path.points:
#            demo.DrawLine(nmath.Point(p[0], 0.1, p[1]), nmath.Point(prev_p[0], 0.1, prev_p[1]), 4.0, nmath.Vec4(1,0,0,1))
#            prev_p = p
