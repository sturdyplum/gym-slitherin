import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import spaces
import random
import pygame
import operator
import numpy as np

class Snake(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.number_of_snakes = 1
        self.number_of_food = 1
        self.world_size = 10
        self.first = True
        self.move_tuple = [(0,1), (0,-1), (1,0), (-1,0)]
        self.observation_space = spaces.Box(low=-0.0, high=1.0, shape=(self.number_of_snakes + 1, self.world_size, self.world_size), dtype=np.float32)
        self.action_space = spaces.Discrete(4)
        self.reset()

    def dead(self, location):
        return not self.valid_range(location) or self.world[location[0], location[1]] > 1

    def valid_range(self, location):
        return min(location[0],location[1]) >= 0 and max(location[0],location[1]) < self.world_size

    # actions here should be a list of actions for every single agent
    def step(self, action):
        for i in self.alive:
            assert(action >= 0 and action <= 3)
            self.positions[i].append(tuple(map(operator.add, self.positions[i][-1], self.move_tuple[action])))
            if self.valid_range(self.positions[i][-1]):
                self.world[self.positions[i][-1][0]][self.positions[i][-1][1]] += 1
            if self.length[i] < len(self.positions[i]):
                self.world[self.positions[i][0][0]][self.positions[i][0][1]] -= 1
                self.positions[i].pop(0)

        # Need to keep track of which snakes will die and kill them later so
        # that if two snakes run into each other they both die not just one.
        new_dead = []
        for i in self.alive:
            if self.dead(self.positions[i][-1]):
                new_dead.append(i)

        for i in new_dead:
            self.alive.remove(i)
            self.positions[i] = []

        reward = 0
        for i in self.alive:
            if self.eat(self.positions[i][-1]):
                reward += 1
                self.length[i] += 1
                self.food.remove(self.positions[i][-1])

        while len(self.food) < self.number_of_food:
            self.place_food()

        done = False
        if len(self.alive) == 0:
            done = True

        return self.get_state(), reward, done, 0

    def reset(self):
        self.reset_initial_positions()
        self.food = set()
        for _ in range(self.number_of_food):
            self.place_food()
        self.alive = set(range(self.number_of_snakes))
        self.length = [1 for _ in range(self.number_of_snakes)]
        self.world = np.zeros((self.world_size, self.world_size), dtype=np.int)
        return self.get_state()

    def reset_initial_positions(self):
        """
        Fills the self.positions array with the starting positions for all the
        self.number_of_snakes number of snakes.
        """
        # There are length ^ 2 number of unique positions
        pos = list(range(self.world_size ** 2))
        random.shuffle(pos)
        self.positions = [[(pos[i]//self.world_size, pos[i]%self.world_size)] for i in range(self.number_of_snakes)]

    def place_food(self):
        """Adds a single food to the self.food."""
        # randomly placing food should take
        # (on average) O(area / number_of_free slots)
        # So just doing this should be in its worst case, as bad as doing the n^2
        while True:
            spot = random.randint(0, self.world_size ** 2 - 1)
            if self.valid(spot):
                self.food.add((spot % self.world_size, spot // self.world_size))
                return


    def render(self, mode='human'):
        """Using pygame, render the environment to a screen."""

        if self.first:
            pygame.init()
            self.window = pygame.display.set_mode((1000,1000))
            pygame.display.set_caption("Slitherin")
            self.first = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

        self.window.fill((0,0,0))
        for food in self.food:
            pygame.draw.rect(self.window, (255, 0, 0), (food[0] * 10, food[1] * 10, 10, 10))

        for snake in self.positions:
            for loc in snake:
                pygame.draw.rect(self.window, (0, 255, 0), (loc[0] * 10, loc[1] * 10, 10, 10))

        pygame.display.update()

    def close(self):
        pass

    def eat(self, location):
        return location in self.food

    def valid(self, location):
        cord = (location % self.world_size, location // self.world_size)
        return cord not in self.food and self.world[cord[0], cord[1]] == 0

    def get_state(self):
        """
        Returns a [number_of_snakes + 1, length, length] numpy array. For the
        First number_of_snakes arrays it will simply be a matrix representing
        the positions of the ith snake. The last array will have the poistions
        all the food.
        """
        state = np.zeros((self.number_of_snakes + 1, self.world_size, self.world_size),dtype=np.float32)
        for i in range(self.number_of_snakes):
            for loc in self.positions[i]:
                state[i][loc[0]][loc[1]] = 1.0

        for food in self.food:
            state[-1][food[0]][food[1]] = 1.0

        return state
