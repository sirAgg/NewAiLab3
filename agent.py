import pygame
import a_star

import math

start_x = 0
start_y = 0

draw_all = None


class Agent:
    def __init__(self, board):
        self.x = start_x
        self.y = start_y
        
        self.following_path = False
        self.speed = 0.1
        self.path = None
        self.ast = None

    def update(self, dt, board):

        if self.following_path: 
            speed = self.speed * dt

            if board[int(self.x)][int(self.y)][0] == "G":
                speed *= 0.5

            while 1: 
                if not self.path.points: 
                    self.following_path = False
                    self.following_path_callback()
                    return
                p = (self.path.points[0][0] + 0.5, self.path.points[0][1] + 0.5)
                dx = p[0] - self.x
                dy = p[1] - self.y
                d = math.sqrt(dx*dx + dy*dy)

                if d > speed:
                    break

                speed -= d

                self.x = p[0]
                self.y = p[1]
                self.path.points.pop(0)

            d = math.sqrt(dx*dx + dy*dy)
            self.x += dx*speed/d
            self.y += dy*speed/d

    
    def move_to(self, board, callback, x, y):
        self.path = a_star.Path((int(self.x), int(self.y)), (int(x),int(y)))

        self.ast = None
        self.ast = a_star.AStar()
        self.ast.start(self.path, board)

        while not self.ast.step(self.path, board):
            #draw_all()
            pass

        self.following_path = True
        self.following_path_callback = callback

    def move_towards(self, dt, board, p):
        speed = self.speed * dt

        if board[int(self.x)][int(self.y)][0] == "G":
            speed *= 0.5

        dx = p[0] - self.x
        dy = p[1] - self.y
        d = math.sqrt(dx*dx + dy*dy)
        nx = self.x + dx/d*speed
        ny = self.y + dy/d*speed

        if board[int(nx)][int(ny)][0] in "VB":
            return False

        if (int(nx), int(ny)) == (int(p[0]), int(p[1])):
            return False

        self.x = nx
        self.y = ny

        return True


    def draw(self, surface, color):
        pygame.draw.rect(surface, color, pygame.Rect(self.x*8 - 2, self.y*8 - 2, 4, 4))
        pygame.draw.circle(surface, color, (self.x*8,self.y*8), 3)
        #if self.ast:
        #    self.ast.visualize(surface)
        
        if self.path and self.path.points:
            prev_p = self.path.points[0]
            def fix(p):
                return (p[0]*8+4, p[1]*8+4)
            for p in self.path.points:
                pygame.draw.line(surface, (255,0,0), fix(p), fix(prev_p))
                prev_p = p
