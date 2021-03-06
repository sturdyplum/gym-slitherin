from slitherin_env import Slitherin
from snake_env import Snake
import random
env = Snake()
num_snakes = 1

while True:
    actions = [random.randint(0,3) for _ in range(num_snakes)]
    obs, _, done , _ = env.step(actions)
    print(obs.shape)
    env.render()
    if done:
        env.reset()
