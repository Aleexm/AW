import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_aw.create_map import *
from gym_aw.tile import Tile
from gym_aw.unit import *
from gym_aw.terrain import Terrain
from gym_aw.a_star import a_star, traverse_tile_cost
from gym_aw.enums import *
from copy import copy
import math

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
        return self.idtionable_units()

    def get_actionable_units(self):
        actionable = np.zeros(np.shape(self.battlefield))
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                unit = self.battlefield[row][col].unit
                if unit is None or unit.country != self.active_player:
                    continue
                assert not unit.is_selected
                if unit.country == self.active_player:
                    if not unit.has_finished:
                        actionable[row,col] = 1
        return actionable

    def get_reachable_squares(self, unit):
        "TODO: FIX JOIN"
        '''
        For a specific unit, get all reachable squares, taking into account
        its movement, the weather and TODO: (s)COP.

        Args:
            - unit(Unit): The unit that is selected

        Returns:
            - reachable_squares(List(Tile)): the reachable squares
        '''
        assert not unit.has_moved
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
                            if p.unit is not None and p.unit.country == self.active_player: # TODO: JOIN
                                continue
                            reachable_squares.add(p)
        return reachable_squares

    def get_attackable_squares(self, unit):
        "TODO: Still returns tiles containing no units"
        attackable_squares = set()
        x, y = unit.x, unit.y
        for dx in range(-unit.max_range, unit.max_range+1):
            for dy in range(-unit.max_range, unit.max_range+1):
                if abs(dx) + abs(dy) > unit.max_range:
                    continue # Loop over grid of size 2*max_range: Too far
                if abs(dx) + abs(dy) < unit.min_range:
                    continue # Inside min_range (rockets etc)
                if x+dx >= len(self.battlefield) or y+dy >= len(self.battlefield[0]) \
                or x+dx < 0 or y + dy < 0:
                    continue # Out of bounds
                defending_unit = self.battlefield[x+dx][y+dy].unit
                if defending_unit is None:
                    continue
                if defending_unit.country == self.active_player:
                    continue
                if DAMAGE_CHART[unit.type.value, defending_unit.type.value] == 0:
                    continue
                attackable_squares.add(self.battlefield[x+dx][y+dy])
        return attackable_squares


    def create_unit(self, unit):
        self.battlefield[unit.x][unit.y].unit = unit

    def select_unit(self, unit):
        unit.is_selected = True

    def move_unit(self, unit, new_x, new_y):
        self.battlefield[unit.x][unit.y].unit = None
        self.battlefield[new_x][new_y].unit = unit
        unit.x, unit.y = new_x, new_y
        unit.has_moved = True

    def end_turn(self):
        new_country = self.get_new_country()
        self.active_player = new_country
        self.start_turn()

    def start_turn(self):
        self.ready_country_units(self.active_player)

    def get_new_country(self):
        new_country_idx = (self.countries.index(self.active_player) + 1) \
                          % NUM_PLAYERS
        new_country = self.countries[new_country_idx]
        return new_country

    def ready_country_units(self, country):
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                unit = self.battlefield[row][col].unit
                if unit is None or unit.country != country:
                    continue
                unit.ready()

    def check_done(self):
        winner = self.check_unit_victory()
        if winner is not None:
            return True
        winner = self.check_HQ_victory()
        if winner is not None:
            return True
        return False

    def check_HQ_victory(self):
        found_hqs = list()
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                tile = self.battlefield[row][col].terrain
                if isinstance(tile, HQ):
                    found_hqs.append(tile.country)
        if len(found_hqs) < 2:
            return found_hqs[0]
        return None

    def attack_unit(self, attacker_tile, defender_tile):
        "TODO: prev_a_health prev_d_health used for logging only."
        attacker = attacker_tile.unit
        defender = defender_tile.unit
        prev_a_health = copy(attacker.visible_hp)
        prev_d_health = copy(defender.visible_hp)
        attack_damage = self.damage_formula(attacker, defender, defender_tile.terrain)
        defender.hp = max(0, round(defender.hp - attack_damage, 1))
        defender.visible_hp = math.ceil(defender.hp/10)
        if defender.hp == 0:
            self.battlefield[defender_tile.x][defender_tile.y].unit = None
            print("=== {}({}) killed {}".format(attacker, prev_a_health, defender))
        else:
            defense_damage = self.damage_formula(defender, attacker, attacker_tile.terrain)
            attacker.hp = max(0, round(attacker.hp - defense_damage, 1))
            attacker.visible_hp = math.ceil(attacker.hp/10)
            print("=== {}({}) attacked {}({}) for {} vs {}".format(attacker, prev_a_health, defender, prev_d_health, round(attack_damage/10, 2), round(defense_damage/10, 2)))

    def damage_formula(self, attacker, defender, defender_terrain):
        first_term = (DAMAGE_CHART[attacker.type.value, defender.type.value] * 100) / 100 + random.randrange(0,10)
        second_term = attacker.visible_hp / 10
        third_term = (200 - (100 + defender_terrain.defense * defender.visible_hp)) / 100
        return first_term * second_term * third_term

    def check_unit_victory(self):
        found_countries = list()
        found_country = False
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                tile = self.battlefield[row][col]
                if tile.unit is not None:
                    if not found_country:
                        found_countries.append(tile.unit.country)
                        found_country = True
                    else:
                        if tile.unit.country != found_countries[0]:
                            found_countries.append(tile.unit.country)
        if len(found_countries) < 2:
            return found_countries[0]
        return None


    def __repr__(self):
        res = ''
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                res += '{} \n'.format(str(self.battlefield[row][col]))
        return res
