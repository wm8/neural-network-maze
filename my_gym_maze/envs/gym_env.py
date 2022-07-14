import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from my_gym_maze.envs.maze_view_2d import MazeView2D
from my_gym_maze.envs.hunt_and_kill import Hund_And_Kill


class MazeEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    ACTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, maze_algorithm="hunt_and_kill", maze_size=None, enable_render=True):

        self.viewer = None
        self.enable_render = enable_render
        maze = None
        if maze_algorithm == "hunt_and_kill":
            maze = Hund_And_Kill(maze_size[0], maze_size[1])
        if maze_size[0] < maze_size[1]:
            screen_size = (int(600 * (maze_size[1] / maze_size[0])), 600)
        else:
            screen_size = (600, int(600 * (maze_size[0] / maze_size[1])))
        self.maze_view = MazeView2D(maze=maze, maze_name="OpenAI Gym - Maze (%d x %d)" % maze_size,
                                    screen_size=screen_size)

        self.maze_size = self.maze_view.maze_size

        # forward or backward in each dimension
        self.action_space = spaces.Discrete(2 * len(self.maze_size))  # =4

        # observation is the x, y coordinate of the grid
        low = np.zeros(len(self.maze_size), dtype=int)
        high = np.array(self.maze_size, dtype=int) - np.ones(len(self.maze_size), dtype=int)
        self.observation_space = spaces.Box(low, high, dtype=np.int64)

        # initial condition
        self.state = None
        self.steps_beyond_done = None

        # Simulation related variables.
        self.seed()
        self.reset()

        # Just need to initialize the relevant attributes
        self.configure()

    def __del__(self):
        if self.enable_render is True:
            self.maze_view.quit_game()

    def configure(self, display=None):
        self.display = display

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):

        if not isinstance(action, (int, int)):
            raise Exception("action type is wrong")
        self.maze_view.move_robot(action)

        if np.array_equal(self.maze_view.robot, self.maze_view.goal):
            reward = 1
            done = True
        else:
            reward = -0.1 / (self.maze_size[0] * self.maze_size[1])
            done = False

        self.state = self.maze_view.robot

        info = {}

        return self.state, reward, done, info

    def reset(self):
        self.maze_view.reset_robot()
        self.state = np.zeros(2)
        self.steps_beyond_done = None
        self.done = False
        return self.state

    def is_game_over(self):
        return self.maze_view.game_over

    def render(self, mode="human", close=False):
        if close:
            self.maze_view.quit_game()

        return self.maze_view.update(mode)


class MazeEnvSample5x5(MazeEnv):
    def __init__(self, enable_render=True):
        super(MazeEnvSample5x5, self).__init__(enable_render=enable_render, maze_size=(5, 5))
