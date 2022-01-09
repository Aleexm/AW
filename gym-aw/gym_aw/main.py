# import pygame
import sys
import numpy
import os
import random
from create_map import *
from dicts import TERRAIN_DICT
from gym_aw.terrain import Terrain
from unit import *
from tile import Tile
import gym
from gym_aw.envs.aw_env import AwEnv
from encode_state import *
from a_star import *
from enums import *
from random_agent import RandomAgent


for i in range(1000):
    if i%100 ==0:
        print(i)


    env = AwEnv('simple_2_inf')
    agent_1 = RandomAgent(1)
    agent_2 = RandomAgent(2)
    agents = [agent_1, agent_2]
    infs = [Recon(Country.GreenEarth,2,1),
            Infantry(Country.GreenEarth,2,0),
            Tank(Country.YellowComet,2,3)]
    for inf in infs:
        env.create_unit(inf)
    done = False
    while not done:
        a = agents[env.countries.index(env.active_player)].act(env)
        done = env.step(a)
    print('============= GAME CONCLUDED =============')
#
# inf1 = Infantry(1,0,0)
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
#
# inf.movement = 5
# inf.movetype = Movetype.Air
# movable_squares = env.get_reachable_squares(inf)
# move_field = np.zeros(np.shape(env.battlefield))
# for sq in movable_squares:
#     move_field[sq.x,sq.y] = 1
# print(move_field)
