import agent
import random
import pygame
import a_star
import worker
import math

class Scout:
    def __init__(self, agent):
        self.agent = agent
        self.agent.speed = 0.2
        self.goal_pos = (random.randint(1, a_star.board_w-1) + 0.5, random.randint(1, a_star.board_h-1) + 0.5)
        self.upgrade_time = 0

    def update(self, dt, board):
        if self.upgrade_time < 60:
            self.upgrade_time += dt
            return

        self.agent.update(dt, board)

        if not self.agent.move_towards(dt, board, self.goal_pos):
            #self.goal_pos = (random.randint(1, a_star.board_w-1) + 0.5, random.randint(1, a_star.board_h-1) + 0.5)
            r = random.random()
            self.goal_pos = (150 * math.cos(r*2*math.pi), 150 * math.sin(r*2*math.pi))
            


        for x, y in [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(0,0)]:
            board[int(self.agent.x) + x][int(self.agent.y) + y][1] = False

            if board[int(self.agent.x) + x][int(self.agent.y) + y][0] == "T":
                board[int(self.agent.x) + x][int(self.agent.y) + y][0] = "5"
                worker.add_tree((int(self.agent.x) + x, int(self.agent.y) + y))


    def draw(self, surface):
        self.agent.draw(surface, (255,255,0,0));
        pygame.draw.circle(surface, (255,0,0), (self.goal_pos[0]*8, self.goal_pos[1]*8), 3)
