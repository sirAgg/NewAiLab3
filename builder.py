import agent
import inventory
import a_star
import worker

N_MAX_BUILDINGS = 3
n_buildings = 0

def UpgradeState(builder, dt, board):
    if builder.upgrade_time > 120:
        return WaitForResourcesState
    builder.upgrade_time += dt
    return UpgradeState

def FindSpotState(builder, dt, board):
    if not builder.found_spot:
        # breadth first search for finding closest empty spot
        possible_spots = [(int(agent.start_x), int(agent.start_y))]
        checked_spots = set()
        
        while possible_spots:
            p = possible_spots.pop(0)
            if p in checked_spots:
                continue

            if board[p[0]][p[1]][0] == "M":
                builder.build_slot = p
                builder.found_spot = True

                def callback():
                    builder.done_path = True

                builder.agent.move_to(board, callback, builder.build_slot[0], builder.build_slot[1]) 

                return FindSpotState

            for n in reversed(a_star.neighbours):
                if not a_star.check_neighbour(board, p[0],p[1], n[0],n[1] ):
                    continue
                possible_spots.append((p[0]+n[0], p[1]+n[1]))

            checked_spots.add(p)

        return FindSpotState

    if builder.done_path:
        builder.found_spot = False
        builder.done_path = False
        return BuildState

    return FindSpotState


def BuildState(builder, dt, board):
    if builder.build_time > 60:
        builder.build_time = 0
        board[ builder.build_slot[0] ][ builder.build_slot[1] ][0] = "K"
        worker.needs_craftmen.append(builder.build_slot)
        global n_buildings
        n_buildings += 1
        return WaitForResourcesState

    builder.build_time += dt

    return BuildState


def WaitForResourcesState(builder, dt, board):
    if n_buildings >= N_MAX_BUILDINGS:
        return WaitForResourcesState
    if inventory.n_logs >= 10:
        inventory.n_logs -= 10
        return FindSpotState

    return WaitForResourcesState


class Builder:
    def __init__(self, agent):
        self.agent = agent
        self.found_spot = False
        self.done_path  = False
        self.build_time = 0
        self.upgrade_time = 0
        self.state = WaitForResourcesState

    def update(self, dt, board):
        self.agent.update(dt, board)
        self.state = self.state(self, dt, board)

    def draw(self, surface):
        self.agent.draw(surface, (0,255,255))
