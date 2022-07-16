import random
from my_gym_maze.envs.Cell import Cell
# import cv2
# import numpy as np
from my_gym_maze.envs.maze import Maze

class Eller(Maze):
    def __init__(self, height, width, path, displayMaze):
        super().__init__(width, height)
        if width % 2 != 0:
            width += 1
        if height % 2 != 0:
            height += 1
        self.width = width
        self.height = height
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
        maze = [[Cell(False, True) for _ in range(self.width)] for _ in range(self.height)]
        cid = 1
        length = 0
        last_eaten_id = 0
        has_b = False
        for y in range(self.height):
            for x in range(self.width):
                if y == 0:
                    if x == 0:
                        continue
                    # Поставить ли границу справа
                    if random.random() > 0.5:
                        # Убираем нижную стену у случайной ячейки множества если множество не имеет выхода вниз
                        if y != self.height - 1 and not has_b:
                            rand_x = random.randint(x - length, x)
                            maze[y][rand_x].down = False
                            maze[y + 1][rand_x].id = cid
                        cid += 1
                        length = 0
                        has_b = False
                        maze[y][x].right = True
                    maze[y][x].id = cid
                    length += 1
                else:
                    # Если сосед справа является частью подмножества, которое начали поглащать
                    if last_eaten_id != 0 and x != self.width - 1 and maze[y][x + 1].id == last_eaten_id:
                        maze[y][x + 1].id = cid
                        length += 1
                    else:
                        last_eaten_id = 0
                        # Поставить ли стену
                        if random.random() > 0.5:
                            # Убираем нижную стену у случайной ячейки множества если множество не имеет выхода вниз
                            if y != self.height - 1 and not has_b:
                                rand_x = random.randint(x - length, x)
                                maze[y][rand_x].down = False
                                maze[y + 1][rand_x].id = cid
                            cid += 1
                            length = 0
                            has_b = False
                            maze[y][x].right = True
                        else:
                            if x != self.width - 1 and maze[y][x + 1].id != 0:
                                last_eaten_id = maze[y][x + 1].id
                            maze[y][x].id = cid
                            length += 1
                    if y == self.height - 1:
                        continue
                    # Убираем ли нижуню границу
                    if random.random() > 0.5:
                        maze[y][x].down = False
                        has_b = True
                        maze[y + 1][x].id = cid
                    # Для крайнего правого подмножества проверяем выход вниз
                    if x == self.width - 1 and not has_b:
                        rand_x = random.randint(x - length, x)
                        maze[y][rand_x].down = False
                        maze[y + 1][rand_x].id = cid
        self.maze = maze
        self.showMaze()
