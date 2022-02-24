import pygame
from pygame.locals import *
import random

import agent
import a_star

board = []
board_w = 0
board_h = 0

with open("lab3_map.txt") as map_file:
    lines = map_file.readlines()
    board_h = len(lines)
    board_w = len(lines[0]) - 1  # -1 to avoid new line char
    board = [list(x) for x in zip(*lines)] # transpose board

agent.start_x = random.randint(1, board_w-2)
agent.start_y = random.randint(1, board_h-2)
a_star.board_w = board_w
a_star.board_h = board_h

pygame.init()
timer = pygame.time.Clock()
window = pygame.display.set_mode( (board_w*8, board_h*8))
pygame.display.set_caption("Ai lab 3")

a = agent.Agent()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    window.fill((0,0,0))
        
    for x in range(0, board_w):
        for y in range(0, board_h):
            if (board[x][y] == "T"):
                pygame.draw.rect(window, (26,102,0), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y] == "V"):
                pygame.draw.rect(window, (86,191,240), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y] == "G"):
                pygame.draw.rect(window, (54,42,34), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y] == "B"):
                pygame.draw.rect(window, (120,120,120), pygame.Rect(x*8,y*8,8,8))
            else:
                pygame.draw.rect(window, (22,168,0), pygame.Rect(x*8,y*8,8,8))

    a.draw(window)

    pygame.display.update()
    timer.tick(60)
