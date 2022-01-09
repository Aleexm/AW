import numpy as np
from consts import *

def encode_state(env):
    '''
    20 x W x L: neutral shit    (float indicates capture points / HP)
    7  x W x L: my properties   (^)
    25 x W x L: my units        (float indicates hp/10)
    7  x W x L: opp properties
    25 x W x L: opp units
    W x L:      ready units
    W x L:      selected unit
    W x L:      selected unit has moved (all 0s / 1s)
    TODO: Fuel / Ammo / CO / Funds / Income
    '''
    state = np.zeros([86, MAX_X, MAX_Y])

    for row in range(len(env.battlefield)):
        for col in range(len(env.battlefield[row])):
            fill_terrain_state(env.battlefield[row][col].terrain,
                               env.active_player, state)
            fill_unit_state(env.battlefield[row][col].unit,
                            env.active_player, state)
            fill_ready_unit_state(env.battlefield[row][col].unit,
                                  env.active_player, state)
            apply_unit_selected_filter(env.battlefield[row][col].unit, state)
    apply_unit_moved_filter(env, state)
    return state


def fill_terrain_state(terrain, active_player, state):
    '''
    Encodes the current terrain tile into the state matrix
    Args:
        - terrain(Terrain): current tile
        - active_player(int): player to move (represented by country 1:16)
        - state(3d numpy array): encoded state (see encode_state())
    '''
    x, y = terrain.x, terrain.y
    if not terrain.is_property: # Regular terrain (plain etc)
        state[terrain.type.encode_idx, x, y] = 1
    else: # Property
        cpt_points = terrain.capture_points / 20 # encoded in [0,1]
        if terrain.country == 0: # Neutral
            state[terrain.type.encode_idx, x, y] = cpt_points
        elif terrain.country == active_player: # My prop
            state[MY_PROP_IDX + (terrain.type.encode_idx - NUM_TERRAINS), x, y] \
            = cpt_points
        else: # Opp prop
            state[OPP_PROP_IDX + (terrain.type.encode_idx - NUM_TERRAINS), x, y] \
            = cpt_points

def fill_unit_state(unit, active_player, state):
    '''
    Encodes the current unit into the state matrix
    Args:
        - unit(Unit): current unit
        - active_player(int): player to move (represented by country 1:16)
        - state(3d numpy array): encoded state (see encode_state())
    '''
    if unit is None:
        return
    x, y = unit.x, unit.y
    encoded_hp = unit.visible_hp / 10 # Units are represented as float (0,1) based on hp
    if unit.country == active_player:
        state[MY_UNIT_IDX + unit.type.value, x, y] = encoded_hp
        if not unit.has_finished:
            state[READY_UNIT_IDX, x, y] = 1
    else:
        state[OPP_UNIT_IDX + unit.type.value, x, y] = encoded_hp

def fill_ready_unit_state(unit, active_player, state):
    if unit.country == active_player and not unit.has_finished:
        state[READY_UNIT_IDX, unit.x, unit.y] = 1

def apply_unit_selected_filter(unit, state):
    "If this unit is currently selected, place a 1 at its location"
    if unit.is_selected:
        state[SELECTED_UNIT_IDX, unit.x, unit.y] = 1

def apply_unit_moved_filter(env, state):
    "All 0s or all 1s"
    if env.unit_moved:
        state[MOVED_UNIT_IDX,:,:] = 1

def encode_set_of_tiles(env, reachable_squares):
    encoded = np.zeros([MAX_X, MAX_Y])
    for tile in reachable_squares:
        encoded[tile.x, tile.y] = 1
    return encoded
