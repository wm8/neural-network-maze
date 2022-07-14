import numpy as np
import pygame


class MazeView2D:
    ACTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, maze,  maze_name="Maze2D", screen_size=(600, 600), enable_render=True):

        # PyGame configurations
        self.__maze = maze
        pygame.init()
        pygame.display.set_caption(maze_name)
        self.clock = pygame.time.Clock()
        self.__game_over = False
        self.__enable_render = enable_render

        self.maze_size = [maze.height, maze.width]
        if self.__enable_render is True:
            # to show the right and bottom border
            self.screen = pygame.display.set_mode(screen_size)
            self.__screen_size = tuple(map(sum, zip(screen_size, (-1, -1))))

        # Set the starting point
        self.__entrance = np.zeros(2, dtype=int)

        # Set the Goal
        self.__goal = np.array(self.maze_size) - np.array((1, 1))

        # Create the Robot
        self.__robot = np.zeros(2, dtype=int)

        if self.__enable_render is True:
            # Create a background
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255, 255, 255))

            # Create a layer for the maze
            self.maze_layer = pygame.Surface(self.screen.get_size()).convert_alpha()
            self.maze_layer.fill((0, 0, 0, 0,))

            # show the maze
            self.__draw_maze()

            # show the robot
            self.__draw_robot()

            # show the entrance
            self.__draw_entrance()

            # show the goal
            self.__draw_goal()

    def update(self, mode="human"):
        try:
            img_output = self.__view_update(mode)
            self.__controller_update()
        except Exception as e:
            self.__game_over = True
            self.quit_game()
            raise e
        else:
            return not self.__game_over

    def quit_game(self):
        try:
            self.__game_over = True
            if self.__enable_render is True:
                pygame.display.quit()
            pygame.quit()
        except Exception as e:
            print("Quit exception: " + e.args[0])
            pass

    def move_robot(self, action):
        if isinstance(action, int):
            action = self.ACTION[action]
        if not self.__maze.canGo(self.robot, (action[0], action[1])):
            return -1
        # update the drawing
        self.__draw_robot(transparency=0)
        # move the robot
        self.__robot += [action[0], action[1]]
        self.__draw_robot(transparency=255)
        return 1
            # print("Wins!")
            # self.__game_over = True
            # self.quit_game()

    def reset_robot(self):

        self.__draw_robot(transparency=0)
        self.__robot = np.zeros(2, dtype=int)
        self.__draw_robot(transparency=255)

    def __controller_update(self):
        if not self.__game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_over = True
                    self.quit_game()
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_DOWN:
                #         self.move_robot(1, 0)
                #     if event.key == pygame.K_UP:
                #         self.move_robot(-1, 0)
                #     if event.key == pygame.K_RIGHT:
                #         self.move_robot(0, 1)
                #     if event.key == pygame.K_LEFT:
                #         self.move_robot(0, -1)

    def __view_update(self, mode="human"):
        if not self.__game_over:
            # update the robot's position
            self.__draw_entrance()
            self.__draw_goal()
            self.__draw_robot()
            # update the screen
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.maze_layer, (0, 0))

            if mode == "human":
                pygame.display.flip()

            return np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface())))

    def __draw_maze(self):

        if self.__enable_render is False:
            return

        line_colour = (0, 0, 0, 255)

        # drawing the horizontal lines
        for y in range(self.maze.height + 1):
            pygame.draw.line(self.maze_layer, line_colour, (0, y * self.CELL_H),
                             (self.SCREEN_W, y * self.CELL_H))

        # drawing the vertical lines
        for x in range(self.maze.width + 1):
            pygame.draw.line(self.maze_layer, line_colour, (x * self.CELL_W, 0),
                             (x * self.CELL_W, self.SCREEN_H))

        # breaking the walls
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                self.__cover_walls(x, y)

    def __cover_walls(self, x, y, colour=(0, 0, 255, 15)):
        dx = x * self.CELL_W
        dy = y * self.CELL_H
        line_head, line_tail = 0, 0
        if not self.maze.maze[y][x].right:
            line_head = (dx + self.CELL_W, dy + 1)
            line_tail = (dx + self.CELL_W, dy + self.CELL_H - 1)
            pygame.draw.line(self.maze_layer, colour, line_head, line_tail)

        if not self.maze.maze[y][x].down:
            line_head = (dx + 1, dy + self.CELL_H)
            line_tail = (dx + self.CELL_W - 1, dy + self.CELL_H)
            pygame.draw.line(self.maze_layer, colour, line_head, line_tail)
        # if not self.maze.maze[y][x].up:
        #     line_head = (dx + 1, dy)
        #     line_tail = (dx + self.CELL_W - 1, dy)
        # if not self.maze.maze[y][x].left:
        #     line_head = (dx, dy + 1)
        # #     line_tail = (dx, dy + self.CELL_H - 1)
        # if line_head != 0 or line_tail != 0:
        #     pygame.draw.line(self.maze_layer, colour, line_head, line_tail)

    def __draw_robot(self, colour=(0, 0, 150), transparency=255):

        y = int(self.__robot[0] * self.CELL_W + self.CELL_W * 0.5 + 0.5)
        x = int(self.__robot[1] * self.CELL_H + self.CELL_H * 0.5 + 0.5)
        r = int(min(self.CELL_W, self.CELL_H) / 5 + 0.5)

        pygame.draw.circle(self.maze_layer, colour + (transparency,), (x, y), r)

    def __draw_entrance(self, colour=(0, 0, 150), transparency=235):

        self.__colour_cell(self.entrance, colour=colour, transparency=transparency)

    def __draw_goal(self, colour=(150, 0, 0), transparency=235):

        self.__colour_cell(self.goal, colour=colour, transparency=transparency)

    def __draw_portals(self, transparency=160):

        if self.__enable_render is False:
            return

        colour_range = np.linspace(0, 255, len(self.maze.portals), dtype=int)
        colour_i = 0
        for portal in self.maze.portals:
            colour = ((100 - colour_range[colour_i]) % 255, colour_range[colour_i], 0)
            colour_i += 1
            for location in portal.locations:
                self.__colour_cell(location, colour=colour, transparency=transparency)

    def __colour_cell(self, cell, colour, transparency):

        if self.__enable_render is False:
            return

        if not (isinstance(cell, (list, tuple, np.ndarray)) and len(cell) == 2):
            raise TypeError("cell must a be a tuple, list, or numpy array of size 2")
        x = int(cell[1] * self.CELL_W + 0.5 + 1 + 0.01 * self.CELL_W)
        y = int(cell[0] * self.CELL_H + 0.5 + 1 + 0.01 * self.CELL_W)
        w = int(self.CELL_W + 0.5 - 1 - 0.02 * self.CELL_W)
        h = int(self.CELL_H + 0.5 - 1 - 0.02 * self.CELL_H)
        pygame.draw.rect(self.maze_layer, colour + (transparency,), (x, y, w, h))

    @property
    def maze(self):
        return self.__maze

    @property
    def robot(self):
        return self.__robot

    @property
    def entrance(self):
        return self.__entrance

    @property
    def goal(self):
        return self.__goal

    @property
    def game_over(self):
        return self.__game_over

    @property
    def SCREEN_SIZE(self):
        return tuple(self.__screen_size)

    @property
    def SCREEN_W(self):
        return int(self.SCREEN_SIZE[0])

    @property
    def SCREEN_H(self):
        return int(self.SCREEN_SIZE[1])

    @property
    def CELL_W(self):
        return float(self.SCREEN_W) / float(self.maze.width)

    @property
    def CELL_H(self):
        return float(self.SCREEN_H) / float(self.maze.height)