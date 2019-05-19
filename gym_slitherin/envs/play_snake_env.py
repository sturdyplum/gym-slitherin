import pygame
from snake_env import Snake
pygame.init()

env = Snake()
done = False
while not done:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    action = 0
    if keys[pygame.K_LEFT]:
        action = 2
    if keys[pygame.K_RIGHT]:
        action = 1

    _, _, done, _ = env.step(action)
    env.render()
