from gym.envs.registration import register

register(
    id='slitherin-v0',
    entry_point='gym_slitherin.envs:Slitherin',
)
