import pygame
from pygame.locals import *
import random

import agent
import a_star
import scout
import worker
import builder
import craftsmen

board = []
board_w = 0
board_h = 0

with open("lab3_map.txt") as map_file:
    lines = map_file.readlines()
    board_h = len(lines)
    board_w = len(lines[0]) - 1  # -1 to avoid new line char
    board = [list(map(lambda e: [e, True], list(x))) for x in zip(*lines)] # transpose board and add bool to every element for fog of war

agent.start_x = random.randint(1, board_w-2)
agent.start_y = random.randint(1, board_h-2)

for x, y in [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(0,0)]:
    board[agent.start_x + x][agent.start_y + y][1] = False

a_star.board_w = board_w
a_star.board_h = board_h

pygame.init()
timer = pygame.time.Clock()
window = pygame.display.set_mode( (board_w*8, board_h*8))
pygame.display.set_caption("Ai lab 3")
fow_surface = pygame.Surface( (board_w*8, board_h*8), pygame.SRCALPHA)

agents = []
for _ in range(3):
    agents.append(scout.Scout(agent.Agent(board)))
for _ in range(1):
    agents.append(builder.Builder(agent.Agent(board)))
for _ in range(46):
    agents.append(worker.Worker(agent.Agent(board)))


time_multipliers = [1, 2, 4, 8, 16, 32, 64]
time_mul_idx = 0

done = False

def upgrade_worker_to_craftsmen(worker, kiln_pos):
    c = craftsmen.Craftsmen(worker.agent, kiln_pos)
    agents.remove(worker)
    agents.append(c)

worker.upgrade_worker_to_craftsmen = upgrade_worker_to_craftsmen


def draw_all():
    for x in range(0, board_w):
        for y in range(0, board_h):
            if (board[x][y][0] in "T54321"):
                pygame.draw.rect(window, (26,102,0), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y][0] == "V"):
                pygame.draw.rect(window, (86,191,240), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y][0] == "G"):
                pygame.draw.rect(window, (54,42,34), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y][0] == "B"):
                pygame.draw.rect(window, (120,120,120), pygame.Rect(x*8,y*8,8,8))
            elif board[x][y][0] == "K":
                pygame.draw.rect(window, (131,58,232), pygame.Rect(x*8,y*8,8,8))
            else:
                pygame.draw.rect(window, (22,168,0), pygame.Rect(x*8,y*8,8,8))

            if board[x][y][1]:
                pygame.draw.rect(fow_surface, (0,0,0,180), pygame.Rect(x*8,y*8,8,8))
            else:
                pygame.draw.rect(fow_surface, (0,0,0,0), pygame.Rect(x*8,y*8,8,8))


    for a in agents:
        a.draw(window)

    window.blit(fow_surface, (0,0))

    pygame.display.update()
    timer.tick(30)

agent.draw_all = draw_all

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            elif event.key == K_UP:
                if time_mul_idx < len(time_multipliers)-1:
                    time_mul_idx += 1
            elif event.key == K_DOWN:
                if time_mul_idx > 0:
                    time_mul_idx -= 1


    window.fill((0,0,0))

    dt = timer.get_time() / 1000 * time_multipliers[time_mul_idx]

    if dt > 5:
        dt = 5

    for a in agents:
        a.update(dt, board)

    for x in range(0, board_w):
        for y in range(0, board_h):
            if (board[x][y][0] in "T54321"):
                pygame.draw.rect(window, (26,102,0), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y][0] == "V"):
                pygame.draw.rect(window, (86,191,240), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y][0] == "G"):
                pygame.draw.rect(window, (54,42,34), pygame.Rect(x*8,y*8,8,8))
            elif (board[x][y][0] == "B"):
                pygame.draw.rect(window, (120,120,120), pygame.Rect(x*8,y*8,8,8))
            elif board[x][y][0] == "K":
                pygame.draw.rect(window, (131,58,232), pygame.Rect(x*8,y*8,8,8))
            else:
                pygame.draw.rect(window, (22,168,0), pygame.Rect(x*8,y*8,8,8))

            if board[x][y][1]:
                pygame.draw.rect(fow_surface, (0,0,0,180), pygame.Rect(x*8,y*8,8,8))
            else:
                pygame.draw.rect(fow_surface, (0,0,0,0), pygame.Rect(x*8,y*8,8,8))

    for a in agents:
        a.draw(window)

    window.blit(fow_surface, (0,0))

    pygame.display.update()
    timer.tick(30)
