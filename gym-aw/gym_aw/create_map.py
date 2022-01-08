import numpy as np
import random
from dicts import TERRAIN_DICT
from terrain import *
import os
from consts import *
from enums import *

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
            # square = Terrain(bf[row, col], row, col)
            id = bf[row,col]
            country = get_country(id)
            terrain = create_square(id, row, col, country)
            terrain_bf[row][col] = terrain
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
            if tile_country.value > 0:
                if not found_first:
                    first_country = tile_country
                    found_first = True
                else:
                    if tile_country != first_country:
                        second_country = tile_country
    if first_country.value < second_country.value:
        return (first_country, second_country)
    else:
        return (second_country, first_country)

def create_square(id, x, y, country):
    "Remaps AWBW ids to actual terrain Types"
    if id == 1:
        return Plain(x, y, country)
    if id == 2:
        return Mountain(x, y, country)
    if id == 3:
        return Wood(x, y, country)
    if id in list(range(4,15)):
        return River(x, y, country)
    if id in list(range(15,26)):
        return Road(x, y, country)
    if id in [26, 27]:
        return Bridge(x, y, country)
    if id == 28:
        return Sea(x, y, country)
    if id in list(range(29,33)):
        return Shoal(x, y, country)
    if id == 33:
        return Reef(x, y, country)
    if id in [34, 38, 43, 48, 53, 81, 86, 91, 96, 119, 124, 151, 158, 165, 172, 183, 190]:
        return City(x, y, country)
    if id in [35, 39, 44, 49, 54, 82, 87, 92, 97, 118, 123, 150, 157, 164, 171, 182, 189]:
        return Base(x, y, country)
    if id in [36, 40, 45, 50, 55, 83, 88, 93, 98, 117, 122, 149, 156, 163, 170, 181, 188]:
        return Airport(x, y, country)
    if id in [37, 41, 46, 51, 56, 84, 89, 94, 99, 121, 126, 155, 162, 169, 176, 187, 194]:
        return Port(x, y, country)
    if id in [127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 152, 159, 166, 173, 184, 191]:
        return Comtower(x, y, country)
    if id in [138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 154, 161, 168, 175, 186, 193]:
        return Lab(x, y, country)
    if id in [42, 47, 52, 57, 85, 90, 95, 100, 120, 125, 153, 160, 167, 174, 185, 192]:
        return HQ(x, y, country)
    if id in list(range(101, 111)):
        return Pipe(x, y, country)
    if id in [113, 114]:
        return Pipeseam(x, y, country)
    if id in [115, 116]:
        return Rubble(x, y, country)
    if id in [111, 112]:
        return Missile(x, y, country)

def get_country(id):
    "see https://awbw.amarriner.com/countries.php"
    if id in [34,35,36,37,133,145]:
        return Country.Neutral
    if id in [38,39,40,41,42,134,146]:
        return Country.OrangeStar
    if id in [43,44,45,46,47,129,140]:
        return Country.BlueMoon
    if id in [48,49,50,51,52,131,142]:
        return Country.GreenEarth
    if id in [53,54,55,56,57,136,148]:
        return Country.YellowComet
    if id in [91,92,93,94,95,128,139]:
        return Country.BlackHole
    if id in [81,82,83,84,85,135,147]:
        return Country.RedFire
    if id in [86,87,88,89,90,137,143]:
        return Country.GreySky
    if id in [96,97,98,99,100,130,141]:
        return Country.BrownDesert
    if id in [117,118,119,120,121,127,138]:
        return Country.AmberBlaze
    if id in [122,123,124,125,126,132,144]:
        return Country.JadeSun
    if id in [149,150,151,152,153,154,155]:
        return Country.CobaltIce
    if id in [156,157,158,159,160,161,162]:
        return Country.PinkCosmos
    if id in [163,164,165,166,167,168,169]:
        return Country.TealGalaxy
    if id in [170,171,172,173,174,175,176]:
        return Country.PurpleLightning
    if id in [181,182,183,184,185,186,187]:
        return Country.AcidRain
    if id in [188,189,190,191,192,193,194]:
        return Country.WhiteNova
    return Country.NoCountry # Just a terrain tile, no country


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
