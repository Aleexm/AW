import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_aw.create_map import *
from gym_aw.tile import Tile
from gym_aw.unit import *
from gym_aw.terrain import *

class AwEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, map=None, predeployed_units=None):
        if map is not None:
            terrain = create_battlefield_from_data(map)
        else:
            terrain = create_battlefield_random()
        terrain = create_terrain_tiles(terrain)
        self.map_dim = np.shape(terrain)
        if predeployed_units is not None:
            units = load_units()
        else:
            units = [[None for c in range(self.map_dim[1])] for r in range(self.map_dim[0])]
        self.battlefield = [[Tile(terrain[r][c], units[r][c]) for c in range(self.map_dim[1])] for r in range(self.map_dim[0])]
        self.countries = get_1v1_map_countries(terrain)
        self.active_player = self.countries[0]
        self.initial_player = self.active_player

    def step(self, action):
        pass
    def reset(self):
        pass
    def render(self, mode='human', close=False):
        pass

    def get_valid_actions(self):
        '''
        TODO:
        1. L x W: select unit                         +
        2. L x W: move here        (JOIN if unit)     +
        3. L x W: attack here                         +
        4. Wait
        5. Capture
        6. Delete
        7. Submerge / Hide
        8. Unhide
        9. Load unit (On move?)
        10. Drop unit NESW
        11. Repair (bb) NESW
        12. L x W: Launch Silo at square
        13. Explode BB
        14. Resupply NESW
        15. Use COp
        16. Use SCop
        17. Yield
        '''
        return self._get_actionable_units()

    def _get_actionable_units(self):
        actionable = np.zeros(np.shape(self.battlefield))
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                unit = self.battlefield[row][col].unit
                if unit is None:
                    continue
                assert not unit.is_selected
                if unit.country == self.active_player:
                    if not unit.has_finished:
                        actionable[row,col] = 1
        return actionable

    def _get_movable_squares(self):
        pass

    def create_unit(self, unit, x, y):
        self.battlefield[x][y].unit = unit

    def __repr__(self):
        res = ''
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                res += '{} \n'.format(str(self.battlefield[row][col]))
        return res
