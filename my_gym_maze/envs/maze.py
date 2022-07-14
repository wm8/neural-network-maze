from my_gym_maze.envs.Cell import Cell
from my_gym_maze.envs.maze_view_2d import MazeView2D

class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.maze = [[Cell(False, False) for _ in range(self.width)] for _ in range(self.height)]

    def canGo(self, s_pos, delta):
        # Выход за границы
        if delta[0] == -1 and s_pos[0] == 0:
            return False
        if delta[0] == 1 and s_pos[0] == self.height-1:
            return False
        if delta[1] == -1 and s_pos[1] == 0:
            return False
        if delta[1] == 1 and s_pos[1] == self.width-1:
            return False
        # Есть стена снизу
        if delta[0] == 1 and self.maze[s_pos[0]][s_pos[1]].down:
            return False
        # Есть стена сверху
        if delta[0] == -1 and self.maze[s_pos[0]-1][s_pos[1]].down:
            return False
        # Есть стена справа
        if delta[1] == 1 and self.maze[s_pos[0]][s_pos[1]].right:
            return False
        # Есть стена слева
        if delta[1] == -1 and self.maze[s_pos[0]][s_pos[1]-1].right:
            return False
        return True

    def showMaze(self):
        if self.height < self.width:
            screen_size = (int(600*(self.width/self.height)), 600)
        else:
            screen_size = (600, int(600*(self.height/self.width)))
        MazeView = MazeView2D(self, screen_size=screen_size)
        #MazeView = MazeView2D(self)
        while MazeView.update():
            pass