from gym.envs.registration import register

register(
    id='maze-v0',
    entry_point='my_gym_maze.envs.gym_env:MazeEnvSample5x5',
    max_episode_steps=2000,
)