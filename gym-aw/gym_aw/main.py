# import pygame
import numpy as np
import os
import random
from create_map import *
from dicts import TERRAIN_DICT
from terrain import Terrain
from unit import *
from tile import Tile
import gym
from gym_aw.envs.aw_env import AwEnv
from encode_state import *

env = AwEnv('spann_island')
inf1 = Infantry(1,0,0)
inf2 = Infantry(2,1,1)
env.create_unit(inf1, inf1.x, inf1.y)
env.create_unit(inf2, inf2.x, inf2.y)
env.battlefield[inf1.x][inf1.y].unit = inf1
env.battlefield[inf2.x][inf2.y].unit = inf2
state = encode_state(env)
print(state)
