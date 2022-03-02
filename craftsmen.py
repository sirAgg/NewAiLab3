import agent
import inventory
import builder

def UpgradeState(craftsmen, dt, board):
    if craftsmen.upgrade_time > 120:
        return GotoKilnState
    craftsmen.upgrade_time += dt
    return UpgradeState

def GotoKilnState(craftsmen, dt, board):
    def callback():
        craftsmen.done_path = True

    if not craftsmen.found_path:
        craftsmen.agent.move_to(board, callback, craftsmen.kiln_pos[0], craftsmen.kiln_pos[1])
        craftsmen.found_path = True

    if craftsmen.done_path:
        craftsmen.found_path = False
        craftsmen.done_path  = False
        return WaitForLogsState

    return GotoKilnState


def WorkState(craftsmen, dt, board):
    if craftsmen.work_timer >= 30:
        craftsmen.work_timer = 0
        inventory.n_charcoal += 1
        print("Charcoal:", inventory.n_charcoal)
        return WaitForLogsState

    craftsmen.work_timer += dt

    return WorkState


def WaitForLogsState(craftsmen, dt, board):
    if builder.n_buildings >= builder.N_MAX_BUILDINGS and inventory.n_logs >= 2:
        inventory.n_logs -= 2
        return WorkState
    return WaitForLogsState


class Craftsmen:
    def __init__(self, agent, kiln_pos):
        self.agent = agent
        self.state = UpgradeState
        self.kiln_pos = kiln_pos
        self.found_path = False
        self.done_path = False
        self.work_timer = 0
        self.upgrade_time = 0
    
    def update(self, dt, board):
        self.agent.update(dt, board)
        self.state = self.state(self, dt, board)

    def draw(self, surface):
        self.agent.draw(surface, (255,0,255))
