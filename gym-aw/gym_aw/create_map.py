import numpy as np
import random
from dicts import TERRAIN_DICT
from terrain import *
import os
from consts import *

def create_battlefield_random(size_x = None, size_y = None, cities = None, bases = None,
                              airports = None, ports = None, comtowers = None):
    "TODO: Some mirroring, type of terrain distribution (balanced city,plains etc)"
    bf = np.random.randint(0,1,(size_x, size_y))
    for i in range(size_x):
        for j in range(size_y):
            valid = False
            while not valid:
                rng = random.randint(1,194)
                if rng not in np.arange(58,81) and rng not in np.arange(177, 181):
                    valid = True
            bf[i,j] = rng
    return bf

def create_battlefield_from_data(map):
    "Loads in map(txt_file) and converts its contents to 2D numpy array"
    file = os.path.join('maps', '{}.txt'.format(map))
    return np.loadtxt(file, delimiter = ',')

def create_terrain_tiles(bf):
    '''
    Converts a battlefield of text (using AWBW map tile indices) to actual
    Terrain tiles that are used throughout this script.

    Args:
        - bf(2D numpy array): Array containing AWBW terrain indices (1 for plain etc)

    Returns
        - terrain_bf(2D List): Each entry contains class Terrain representing
                               the terrain type.
    '''
    terrain_bf = [[None for col in range(np.shape(bf)[1])] for row in range(np.shape(bf)[0])]
    for row in range(len(bf)):
        for col in range(len(bf[row])):
            square = Terrain(bf[row, col], row, col)
            terrain_bf[row][col] = square
    return terrain_bf

def get_1v1_map_countries(bf):
    '''
    Loops over the battlefield to get the two countries, returning Tuple (p1, p2)

    Args:
        - bf(2D List of Terrain): Represents the battlefield's terrain tiles

    Returns:
        - Tuple: First idx is p1 country idx (1-16), second idx is second to act
    '''
    found_first = False
    for row in range(len(bf)):
        for col in range(len(bf[row])):
            tile_country = bf[row][col].country
            if tile_country > 0:
                if not found_first:
                    first_country = tile_country
                    found_first = True
                else:
                    if tile_country != first_country:
                        second_country = tile_country
    return (min(first_country, second_country), max(first_country, second_country))


# def change_countries_to_ge_yc(bf):
#     '''
#     Changes the 2 countries to Green Earth, Yellow Comet respectively.
#     Just makes it easier to program everything.
#
#     Args:
#         - bf: List(List) containing class Terrain tiles
#     '''
#     map_countries = get_1v1_map_countries(bf)
#     for row in range(len(bf)):
#         for col in range(len(bf[row])):
#             current_tile = bf[row][col]
#             if current_tile.country <= 0:
#                 continue
#             if current_tile.country == map_countries[0]:
#                 new_id = change_country(current_tile, 3)
#             elif current_tile.country == map_countries[1]:
#                 new_id = change_country(current_tile, 4)
#             bf[row][col].set_sprite(new_id)
#
# def change_country(tile, new_country):
#     "Remaps AWBW ids to Green Earth / Yelow Comet ids"
#     if isinstance(tile.type, City):
#         if new_country == 3:
#             new_id = 48
#         else:
#             new_id = 53
#     if isinstance(tile.type, Base):
#         if new_country == 3:
#             new_id = 49
#         else:
#             new_id = 54
#     if isinstance(tile.type, Airport):
#         if new_country == 3:
#             new_id = 50
#         else:
#             new_id = 55
#     if isinstance(tile.type, Port):
#         if new_country == 3:
#             new_id = 51
#         else:
#             new_id = 56
#     if isinstance(tile.type, HQ):
#         if new_country == 3:
#             new_id = 52
#         else:
#             new_id = 57
#     if isinstance(tile.type, Lab):
#         if new_country == 3:
#             new_id = 142
#         else:
#             new_id = 148
#     if isinstance(tile.type, Comtower):
#         if new_country == 3:
#             new_id = 131
#         else:
#             new_id = 136
#     return new_id
