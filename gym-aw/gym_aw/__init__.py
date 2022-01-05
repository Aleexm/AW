from gym.envs.registration import register

register(
    id='aw-v0',
    entry_point='gym_aw.envs:AwEnv',
)
