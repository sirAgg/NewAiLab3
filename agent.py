import pygame

start_x = 0
start_y = 0


class Agent:
    def __init__(self):
        self.x = start_x
        self.y = start_y

    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), pygame.Rect(self.x*8 + 3, self.y*8 + 3, 4, 4))
