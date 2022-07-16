from setuptools import setup

setup(name="my_gym_maze",
      version="0.1",
      url="",
      author="Lunev Alexey",
      license="MIT",
      packages=["my_gym_maze", "my_gym_maze.envs"],
      install_requires = ["gym", "pygame", "numpy"]
)
