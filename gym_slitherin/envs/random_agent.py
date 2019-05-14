from slitherin_env import Slitherin
import random
env = Slitherin()
num_snakes = 15

while True:
    actions = [random.randint(0,3) for _ in range(num_snakes)]
    _, _, done , _ = env.step(actions)
    env.render()
    if done:
        env.reset()
