import pygame
import a_star

start_x = 0
start_y = 0


class Agent:
    def __init__(self, board):
        self.x = start_x
        self.y = start_y
        self.path = a_star.Path((self.x, self.y), (1,1))

        self.ast = a_star.AStar()

        self.ast.start(self.path, board)
        while not self.ast.step(self.path, board):
            pass

    def update(self):
        speed = 0.1
        if not self.path.points: 
            return
        p = self.path.points[0]
        dx = p[0] - self.x
        dy = p[1] - self.y
        if abs(dx) < speed and abs(dy) < speed:
            self.x = p[0]
            self.y = p[0]
            self.path.points.pop(0)
            return
        self.x += dx*speed
        self.y += dy*speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), pygame.Rect(self.x*8 + 3, self.y*8 + 3, 4, 4))
        self.ast.visualize(self.path, surface)
