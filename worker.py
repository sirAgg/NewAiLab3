import agent
import inventory
import bisect
import math

upgrade_worker_to_craftsmen = None

found_trees = []
needs_craftmen = []

def add_tree(pos):
    def key(e):
        dx = agent.start_x - e[0][0]
        dy = agent.start_y - e[0][1]
        return math.sqrt(dx*dx + dy*dy)

    v = key([pos, 5])
    for i, e in enumerate(found_trees):
        if v < key(e):
            found_trees.insert(i, [pos, 5])
            break
    else:
        found_trees.append([pos,5])



def WalkToTreeState(worker, dt, board):
    def callback():
        worker.done_path = True

    if not worker.found_path:
        worker.agent.move_to(board, callback, worker.tree_pos[0], worker.tree_pos[1])
        worker.found_path = True

    if worker.done_path:
        worker.found_path = False
        worker.done_path  = False
        return ChopTreeState

    return WalkToTreeState


def ChopTreeState(worker, dt, board):
    if worker.chopping_time > 30:
        worker.chopping_time = 0
        s = board[int(worker.tree_pos[0])][int(worker.tree_pos[1])][0]
        if s == "1":
            s = "M"
        else:
            s = str(int(s)-1)
        board[int(worker.tree_pos[0])][int(worker.tree_pos[1])][0] = s

        return WalkBackState

    worker.chopping_time += dt
    return ChopTreeState


def WalkBackState(worker, dt, board):
    def callback():
        worker.done_path = True

    if not worker.found_path:
        worker.agent.move_to(board, callback, agent.start_x, agent.start_y)
        worker.found_path = True

    if worker.done_path:
        worker.found_path = False
        worker.done_path  = False
        inventory.n_logs += 1
        print("Logs:", inventory.n_logs)
        return WaitForWorkState

    return WalkBackState


def WaitForWorkState(worker, dt, board):
    if needs_craftmen:
        upgrade_worker_to_craftsmen(worker, needs_craftmen.pop(0))
        return None
    if found_trees:
        tree = found_trees[0]
        if tree[1] == 1:
            found_trees.pop(0)
        else:
            found_trees[0][1] -= 1

        worker.tree_pos = tree[0]
        return WalkToTreeState

    return WaitForWorkState


class Worker:
    def __init__(self, agent):
        self.agent = agent
        self.state = WaitForWorkState
        self.found_path = False
        self.done_path  = False
        self.chopping_time = 0

    def update(self, dt, board):
        self.agent.update(dt, board)
        self.state = self.state(self, dt, board)

    def draw(self, surface):
        self.agent.draw(surface, (0,0,255))
