import numpy as np
from consts import *

def encode_state(env):
    '''
    20 x W x L: neutral shit    (float indicates capture points / HP)
    7  x W x L: my properties   (^)
    25 x W x L: my units        (float indicates hp/10)
    7  x W x L: opp properties
    25 x W x L: opp units
    W x L: selected unit
    W x L: square moved to
    '''
    state = np.zeros([86, np.shape(env.battlefield)[0],
                          np.shape(env.battlefield)[1]])

    for row in range(len(env.battlefield)):
        for col in range(len(env.battlefield[row])):
            _fill_terrain_state(env.battlefield[row][col].terrain,
                                env.battlefield, env.active_player, state)
            _fill_unit_state(env.battlefield[row][col].unit,
                             env.battlefield, env.active_player, state)
    return state


def _fill_terrain_state(terrain, bf, active_player, state):
    '''
    Encodes the current terrain tile into the state matrix
    Args:
        - terrain(Terrain): current tile
        - bf(2D List of Tile): Represents the battlefield
        - active_player(int): player to move (represented by country 1:16)
        - state(3d numpy array): encoded state (see encode_state())
    '''
    x, y = terrain.x, terrain.y
    if not terrain.is_property: # Regular terrain terrain (plain etc)
        state[terrain.type.encode_idx, x, y] = 1
    else: # Property
        cpt_points = terrain.capture_points / 20 # encoded in [0,1]
        if terrain.country == 0:
            state[terrain.type.encode_idx, x, y] = cpt_points
        elif terrain.country == active_player: # My prop
            state[MY_PROP_IDX + terrain.type.encode_idx, x, y] = cpt_points
        else: # Opp prop
            state[OPP_PROP_IDX + terrain.type.encode_idx, x, y] = cpt_points

def _fill_unit_state(unit, bf, active_player, state):
    '''
    Encodes the current unit into the state matrix
    Args:
        - unit(Unit): current unit
        - bf(2D List of Tile): Represents the battlefield
        - active_player(int): player to move (represented by country 1:16)
        - state(3d numpy array): encoded state (see encode_state())
    '''
    if unit is None:
        return
    x, y = unit.x, unit.y
    encoded_hp = unit.hp / 10 # Units are represented as float (0,1) based on hp
    if unit.country == active_player:
        state[MY_UNIT_IDX + unit.encode_idx, x, y] = encoded_hp
    else:
        state[OPP_UNIT_IDX + unit.encode_idx, x, y] = encoded_hp
