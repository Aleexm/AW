import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_aw.create_map import *
from gym_aw.tile import Tile
from gym_aw.unit import *
from gym_aw.terrain import *
from a_star import a_star, traverse_tile_cost
from enums import *

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
        self.weather = Weather.Clear

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
        return self.get_actionable_units()

    def get_actionable_units(self):
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

    def get_reachable_squares(self, unit):
        '''
        For a specific unit, get all reachable squares, taking into account
        its movement, the weather and TODO: (s)COP.

        Args:
            - unit(Unit): The unit that is selected

        Returns:
            - reachable_squares(List(Tile)): the reachable squares
        '''
        x, y = unit.x, unit.y
        start = self.battlefield[x][y]
        reachable_squares = set()
        reachable_squares.add(start)
        for dx in range(-unit.movement, unit.movement+1):
            for dy in range(-unit.movement, unit.movement+1):
                if abs(dx) + abs(dy) > unit.movement:
                    continue # Loop over grid of size 2*movement: Too far
                if x+dx >= len(self.battlefield) or y+dy >= len(self.battlefield[0]) \
                or x+dx < 0 or y + dy < 0:
                    continue # Out of bounds
                goal = self.battlefield[x+dx][y+dy]
                if goal in reachable_squares:
                    continue # We've already traveled this tile to a further goal
                path, _ = a_star(start, goal, self.battlefield,
                                 self.active_player, unit, self.weather,
                                 unit.movement) # _ because distance isn't used
                if path is None:
                    continue # Tile is unreachable
                else:
                    for p in path[1:]: # Start tile is already reachable
                        if p not in reachable_squares:
                            reachable_squares.add(p)
        return reachable_squares

    def create_unit(self, unit, x, y):
        self.battlefield[x][y].unit = unit

    def __repr__(self):
        res = ''
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                res += '{} \n'.format(str(self.battlefield[row][col]))
        return res
