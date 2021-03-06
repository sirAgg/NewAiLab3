import enum, math, random
import numpy
import pygame


class TileTypes(enum.auto):
    WALKABLE = 0
    GROUND = 0
    WALL = 0b0000000000010001
    MOUNTAIN = 0b0000000000100001
    WATER = 0b0000000000110001
    QUAGMIRE = 0b0000000001000000
    TREE = 0b0000000001010000
    GOAL = 0b0000000001100000
    START = 0b0000000001110000

    def is_obstructed(t):
        return t & 0b1

    def is_unwalkable(t):
        return (t & 0b11) > 0

    def type(t):
        return t & 0b0000000011110000

    def data(t):
        return (t & 0b1111111100000000) >> 8

    def set_data(t, data):
        return (t & 0b0000000011111111) | (data << 8)

    def is_cloud(t):
        return t & 0b0000000000000010 > 0

    def set_cloud(t):
        return t | 0b0000000000000010

    def unset_cloud(t):
        return t & 0b1111111111111101

    def __eq__(self, t):
        return type(self) == type(t)


class Map:
    def load_from_file(self, filename: str):
        with open(filename) as map_file:

            lines = map_file.readlines()
            h = len(lines)
            w = len(lines[0]) - 1  # -1 to avoid new line char

            self.width = w
            self.height = h

            self.board = numpy.empty((h, w), dtype=numpy.uint16)

            for y, line in enumerate(lines):
                for x, c in enumerate(line):
                    if c == "0":
                        self.board[x][y] = TileTypes.WALKABLE
                    elif c == "X":
                        self.board[x][y] = TileTypes.WALL
                    elif c == "T":
                        self.board[x][y] = TileTypes.set_data(TileTypes.TREE, 5)
                    elif c == "V":
                        self.board[x][y] = TileTypes.WATER
                    elif c == "G":
                        self.board[x][y] = TileTypes.QUAGMIRE
                    elif c == "B":
                        self.board[x][y] = TileTypes.MOUNTAIN
                    elif c == "M":
                        self.board[x][y] = TileTypes.GROUND
                    elif not c == "\n":
                        assert False, "Unknown character in map file."

    def draw(self, surface):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if (self.board[x][y] == TileTypes.GROUND):
                    pygame.draw.rect(surface, (22,168,0), pygame.Rect(x*8,y*8,8,8))
                if (self.board[x][y] == TileTypes.TREE):
                    pygame.draw.rect(surface, (26,255,0), pygame.Rect(x*8,y*8,8,8))
                if (self.board[x][y] == TileTypes.WATER):
                    pygame.draw.rect(surface, (86,191,240), pygame.Rect(x*8,y*8,8,8))
                if (self.board[x][y] == TileTypes.QUAGMIRE):
                    pygame.draw.rect(surface, (54,42,34), pygame.Rect(x*8,y*8,8,8))
                if (self.board[x][y] == TileTypes.MOUNTAIN):
                    pygame.draw.rect(surface, (120,120,120), pygame.Rect(x*8,y*8,8,8))

    def chop_tree(self, x, y):
        tree_tile = self.get(x, y)

        if TileTypes.type(tree_tile) != TileTypes.TREE:
            return False

        n_trees = TileTypes.data(tree_tile)
        n_trees -= 1
        if n_trees <= 0:
            self.set(x, y, TileTypes.GROUND)
            if self.entities[x][y]:
                demo.Delete(self.entities[x][y])
                self.entities[x][y] = None
        else:
            self.set(x, y, TileTypes.set_data(tree_tile, n_trees))

        return True

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.board[y][x]
        return TileTypes.WALL

    def set(self, x: int, y: int, t: TileTypes):
        self.board[y][x] = t

    def uncloud(self, x: int, y: int):
        if x < 0 or self.width <= x or y < 0 or self.height <= y:
            return False

        if TileTypes.is_cloud(self.board[x][y]):
            self.board[x][y] = TileTypes.unset_cloud(self.board[x][y])
            return True
        return False

    def get_neighbours(self, x, y):
        neighbours = []

        tl = True
        tr = True
        bl = True
        br = True

        if self.get(x + 0, y + 1) == TileTypes.WALL:
            br = False
            bl = False
        else:
            neighbours.append((0, 1))

        if self.get(x + 0, y - 1) == TileTypes.WALL:
            tr = False
            tl = False
        else:
            neighbours.append((0, -1))

        if self.get(x + 1, y + 0) == TileTypes.WALL:
            tr = False
            br = False
        else:
            neighbours.append((1, 0))

        if self.get(x - 1, y + 0) == TileTypes.WALL:
            tl = False
            bl = False
        else:
            neighbours.append((-1, 0))

        if br and not self.get(x + 1, y + 1) == TileTypes.WALL:
            neighbours.append((1, 1))
        if bl and not self.get(x - 1, y + 1) == TileTypes.WALL:
            neighbours.append((-1, 1))
        if tr and not self.get(x + 1, y - 1) == TileTypes.WALL:
            neighbours.append((1, -1))
        if tl and not self.get(x - 1, y - 1) == TileTypes.WALL:
            neighbours.append((-1, -1))

        return neighbours

    def check_neighbour(self, x, y, n_x, n_y):
        sx = x + n_x
        sy = y + n_y
        if TileTypes.is_unwalkable(self.get(sx, sy)):
            return False

        if n_x == 0 or n_y == 0:
            return True

        if TileTypes.is_unwalkable(self.get(x, sy)):
            return False

        if TileTypes.is_unwalkable(self.get(sx, y)):
            return False

        return True

map = Map()

