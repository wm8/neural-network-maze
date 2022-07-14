import random
# import numpy as np
# import cv2
from my_gym_maze.envs.Cell import Cell
from my_gym_maze.envs.maze import Maze

class Binary(Maze):
    def __init__(self, height, width, path, displayMaze):
        super().__init__(width, height)
        self.path = path
        self.displayMaze = displayMaze

    # def my_showMaze(self, m):
    #     maze = np.zeros((self.height * 2 + 1, self.width * 2 + 1), dtype=np.float)
    #     x = 1
    #     y = 1
    #     while y != self.height * 2 + 1:
    #         while x != self.width * 2 + 1:
    #             maze[y][x] = 1
    #             if y != self.height * 2 - 1 and not m[y // 2][x // 2].down:
    #                 maze[y + 1][x] = 1
    #             if not m[y // 2][x // 2].right:
    #                 maze[y][x + 1] = 1
    #             x += 2
    #         x = 1
    #         y += 2
    #     cv2.namedWindow('Maze', cv2.WINDOW_NORMAL)
    #     cv2.imshow('Maze', maze)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    def createMaze(self):
        # maze = np.zeros((self.height*2, self.width*2), dtype=np.float)
        self.maze = [[Cell(True, True) for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height-1, -1, -1):
            for x in range(self.width):
                # if x == self.width-1:
                #     self.maze[y][x].down = False
                if y == self.height-1 and x != self.width-1:
                    self.maze[y][x].right = False
                if random.random() > 0.5:
                    if y != self.height-1:
                        self.maze[y][x].down = False
                else:
                    if x != self.width-1:
                        self.maze[y][x].right = False
        #self.my_showMaze(self.maze)
        self.showMaze()
