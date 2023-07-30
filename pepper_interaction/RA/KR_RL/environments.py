from mazelab import BaseMaze
from mazelab import Object
from mazelab import BaseEnv
from mazelab import VonNeumannMotion
import gym
from gym.utils import seeding
from gym.spaces import Box
from gym.spaces import Discrete
from abc import ABC
from abc import abstractmethod
import numpy as np

class MyMaze(BaseMaze):
    def __init__(self, x):
        self.x = x
        super().__init__()
    
    @property
    def size(self):
        return self.x.shape
    
    def make_objects(self):
        free = Object('free', 0, [255, 255, 255], False, np.stack(np.where(self.x == 0), axis=1))
        walls = Object('obstacle1', 1, [160, 160, 160], True, np.stack(np.where(self.x == 1), axis=1))
        agent = Object('agent', 2, [255, 0, 0], False, [])
        garden = Object('obstacle2', 1, [51, 175, 2], True, np.stack(np.where(self.x == 3), axis=1))
        green = Object('obstacle3', 0, [97, 255, 34], False, np.stack(np.where(self.x == 4), axis=1))
        black = Object('obstacle4', 0, [0, 0, 0], False, np.stack(np.where(self.x == 5), axis=1))
        blue = Object('obstacle5', 0, [0, 0, 255], False, np.stack(np.where(self.x == 6), axis=1))
        yellow = Object('obstacle6', 0, [255, 190, 0], False, np.stack(np.where(self.x == 7), axis=1))
        goal = Object('goal', 8, [255, 0, 0], False, [])
        door = Object('obstacle7', 1, [110, 89, 69], True, np.stack(np.where(self.x == 9), axis=1))
        return free, walls, agent, garden, green, black, blue, yellow, goal, door

class BaseEnv(gym.Env, ABC):
    metadata = {'render.modes': ['human', 'rgb_array'],
                'video.frames_per_second' : 3}
    reward_range = (-float('inf'), float('inf'))

    def __init__(self):
        self.viewer = None
        self.seed()

    @abstractmethod
    def step(self, action):
        pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_image(self):
        pass

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

# this is the actual gym environment thanks to which we can train our RL agent
class MyEnv(BaseEnv):
    def __init__(self, x):
        super().__init__()

        self.x = x
        self.maze = MyMaze(self.x)
        self.motions = VonNeumannMotion()

        self.observation_space = Box(low=0, high=len(self.maze.objects), shape=self.maze.size, dtype=np.uint8)
        self.action_space = Discrete(len(self.motions), seed=30)

    def step(self, action):
        motion = self.motions[action]
        current_position = self.maze.objects.agent.positions[0]
        new_position = [current_position[0] + motion[0], current_position[1] + motion[1]]
        
        valid = self.is_valid(new_position)
        if valid:
            self.maze.objects.agent.positions = [new_position]

        if self.is_goal(new_position):
            reward = +1
            done = True
        elif not valid:
            reward = -1
            done = False
        else:
            reward = -0.01
            done = False
        return [current_position, new_position], reward, done, False, {}

    def reset(self):
        start_idx = np.stack(np.where(self.x == 2), axis=1)
        goal_idx = np.stack(np.where(self.x == 8), axis=1)
        self.maze.objects.agent.positions = start_idx
        self.maze.objects.goal.positions = goal_idx
        return self.maze.to_value(), start_idx, goal_idx

    def is_valid(self, position):
        nonnegative = position[0] >= 0 and position[1] >= 0
        within_edge = position[0] < 20 and position[1] < 30
        
        if self.maze.to_value()[position[0]][position[1]] == 1:
            passable = False
        else: 
            passable = True
        return nonnegative and within_edge and passable

    def is_goal(self, position):
        out = False
        for pos in self.maze.objects.goal.positions:
            if position[0] == pos[0] and position[1] == pos[1]:
                out = True
                break
        return out

    def get_image(self):
        return self.maze.to_rgb()