import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random

class Slitherin(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.number_of_snakes = 1
        self.number_of_food = 1
        self.length = 100
        #    self.world = np.zeros((self.world_size, self.world_size))
        self.reset()
        # self.observations_shape
        # self.input_size

    # actions here should be a list of actions for every single agent
    def step(self, action):
        # assert len(action) == self.number_of_snakes
        for i in self.alive:
            # make sure action is in range of [0,3]
            self.positions[i].add(self.positions[i][-1] + move_tuple[action[i]])
            if self.length[i] < self.positions[i]:
                self.positions[i].pop(0)

        # TODO(Pablo) If two snakes run into each other the one with lower index
        # will die. Fix it so that they both die.
        for i in alive:
            # TODO(Pablo) make sure they die if they go off stage (or maybe loop them idk)
            if self.dead(self.positions[i][-1]):
                self.alive.remove(i)
                self.positions[i] = []


        for i in alive:
            if self.eat(self.positions[i][-1]):
                self.length[i] += 1
                self.food.remove(self.positions[i][-1])

        done = False
        if len(self.alive()) == 1:
            done = True

        reward = 0
        if done && 0 in self.alive:
            reward = 1

    # return

    def reset(self):
        self.reset_initial_positions()
        self.reset_initial_food()
        self.alive = set(range(self.number_of_snakes))
        self.length = [1 for _ in range(self.number_of_snakes)]

    def get_initial_positions():
        """
        Fills the self.positions array with the starting positions for all the
        self.number_of_snakes number of snakes.
        """
        # There are length ^ 2 number of unique positions
        pos = range(self.length ** 2)
        random.shuffle(pos)
        self.positions = [(pos[i]/self.length, pos[i]%self.length) for i in range(self.number_of_snakes)

    def get_initial_food():
        """
        Fills the self.positions array with the starting positions for all the
        self.number_of_snakes number of snakes.
        """
        # TODO(Pablo) speed this up n^2 is too slow. Consider using some sort of
        # set of valid positions. Random would work up to some point so maybe
        # that is valid at the beggining. Consider also replacing this with a
        # method that only places 1 food at a time for simplicity.

        ### make sure that we only use valid places
        valid_spots = []
        for i in range(self.length):
            for j in range(self.length):
                if valid

    def render(self, mode='human'):
        """Using pygame, render the environment to a screen."""
        pass

    def close(self):
        pass

    def get_state():
        """
        Returns a [number_of_snakes + 1, length, length] numpy array. For the
        First number_of_snakes arrays it will simply be a matrix representing
        the positions of the ith snake. The last array will have the poistions
        all the food. 
        """
        pass
