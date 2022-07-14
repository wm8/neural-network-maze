from my_gym_maze.envs.maze import Maze
from my_gym_maze.envs.Cell import Cell
from random import choice, randint

class Hund_And_Kill(Maze):
    def __init__(self, height, width):
        super().__init__(width, height)
        self.createMaze()

    def getNeighbors(self, y, x, visited=False):
        n = []
        if not visited:
            if x != 0 and not self.maze[y][x-1].visited:
                n.append((y, x-1))
            if y != 0 and not self.maze[y-1][x].visited:
                n.append((y-1, x))
            if x != self.width-1 and not self.maze[y][x+1].visited:
                n.append((y, x+1))
            if y != self.height-1 and not self.maze[y+1][x].visited:
                n.append((y+1, x))
        else:
            if x != 0 and self.maze[y][x-1].visited:
                n.append((y, x-1))
            if y != 0 and self.maze[y-1][x].visited:
                n.append((y-1, x))
            if x != self.width-1 and self.maze[y][x+1].visited:
                n.append((y, x+1))
            if y != self.height-1 and self.maze[y+1][x].visited:
                n.append((y+1, x))
        return n

    def breakWall(self, p1, p2):
        # Если p2 выше p1, ломаем нижнюю грань p2
        if p1[0] < p2[0]:
            self.maze[p1[0]][p1[1]].down = False
        # Если наоборот, то ломаем грань у p1
        elif p1[0] > p2[0]:
            self.maze[p2[0]][p2[1]].down = False
        # Если p1 правее p2
        if p1[1] > p2[1]:
            self.maze[p2[0]][p2[1]].right = False
        elif p1[1] < p2[1]:
            self.maze[p1[0]][p1[1]].right = False

    def createMaze(self):
        self.maze = [[Cell(True, True) for _ in range(self.width)] for _ in range(self.height)]
        cur_x = randint(0, self.width-1)
        cur_y = randint(0,  self.height-1)
        self.maze[cur_y][cur_x].visited = True
        neighbors = self.getNeighbors(cur_y, cur_x)
        all_visited = False
        while not all_visited:
            while len(neighbors) > 0:
                n = choice(neighbors)
                self.breakWall((cur_y, cur_x), n)
                self.maze[n[0]][n[1]].visited = True
                cur_y, cur_x = n
                neighbors = self.getNeighbors(cur_y, cur_x)
            all_visited = True
            for y in range(self.height):
                for x in range(self.width):
                    if not self.maze[y][x].visited:
                        neighbors = self.getNeighbors(y, x, True)
                        if len(neighbors) < 1:
                            continue
                        all_visited = False
                        n = choice(neighbors)
                        self.breakWall((y, x), n)
                        self.maze[y][x].visited = True
                        cur_y, cur_x = y, x
                        neighbors = self.getNeighbors(y, x)