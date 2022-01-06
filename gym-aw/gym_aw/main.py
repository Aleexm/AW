# import pygame
import sys
import numpy
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
from a_star import *
from enums import Weather

env = AwEnv('spann_island')
# inf1 = Infantry(1,0,0)
inf2 = Infantry(1,5,3)
# tank = Tank(2,0,0)
# recon = Recon(country=0, x=5,y=3)
# env.create_unit(inf1, inf1.x, inf1.y)
# env.create_unit(inf2, inf2.x, inf2.y)
# env.battlefield[inf1.x][inf1.y].unit = inf1
# env.battlefield[inf2.x][inf2.y].unit = inf2
# inf2.hp = 4
# env.battlefield[5][1].terrain.capture_points = 6
# env.battlefield[2][13].terrain.capture_points = 13
# state = encode_state(env)
# print(env.get_valid_actions())

movable_squares = env.get_reachable_squares(inf2)
move_field = np.zeros(np.shape(env.battlefield))
for sq in movable_squares:
    move_field[sq.x,sq.y] = 1
print(move_field)
