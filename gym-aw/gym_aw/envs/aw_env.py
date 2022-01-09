import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_aw.create_map import *
from gym_aw.tile import Tile
from gym_aw.unit import *
from gym_aw.terrain import Terrain
from gym_aw.a_star import a_star, traverse_tile_cost
from gym_aw.enums import *
from gym_aw.encode_state import *
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
        self.selected_unit = None
        self.selected_unit_moved = False

    def step(self, action):
        self.handle_action(action)
        done = self.check_done()
        if self.check_turn_done():
            self.end_turn()
        return done

    def handle_action(self, action):
        window_size = MAX_X * MAX_Y
        window_idx = action // window_size # 0 = select, 1 = move, 2 = attack
        inside_window_idx = action % window_size
        if window_idx == 0: # Select a unit
            selected_unit = self.battlefield[inside_window_idx // MAX_X][inside_window_idx % MAX_X].unit
            self.select_unit(selected_unit)
        elif window_idx == 1: # Move selected unit
            new_tile = self.battlefield[inside_window_idx // MAX_X][inside_window_idx % MAX_X]
            self.move_unit(self.selected_unit, new_tile.x, new_tile.y)
        elif window_idx == 2:
            attacker_tile = self.battlefield[self.selected_unit.x][self.selected_unit.y]
            defender_tile = self.battlefield[inside_window_idx // MAX_X][inside_window_idx % MAX_X]
            self.attack_unit(attacker_tile, defender_tile)
        else:
            self.unready_unit(self.selected_unit)


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
        valid_actions = np.zeros([4, MAX_X, MAX_Y]) # TODO Will not be rect?
        if self.selected_unit is None:
            actionable_units = self.get_actionable_units()
            valid_actions[0] = actionable_units
        if self.selected_unit is not None and not self.selected_unit.has_moved:
            reachable_squares = self.get_reachable_squares()
            encoded_reachable_squares = encode_set_of_tiles(self,
                                                            reachable_squares)
            valid_actions[1] = encoded_reachable_squares
        if self.selected_unit is not None and self.selected_unit.has_moved:
            attackable_squares = self.get_attackable_squares()
            encoded_attackable_squares = encode_set_of_tiles(self,
                                                             attackable_squares)
            valid_actions[2] = encoded_attackable_squares
            valid_actions[3,0,0] = 1 # Temporary wait action at 1st index of 3rd window
        return valid_actions

    def get_actionable_units(self):
        actionable = np.zeros([MAX_X, MAX_Y])
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

    def get_reachable_squares(self):
        "TODO: FIX JOIN"
        '''
        For a specific unit, get all reachable squares, taking into account
        its movement, the weather and TODO: (s)COP.

        Returns:
            - reachable_squares(List(Tile)): the reachable squares
        '''
        unit = self.selected_unit
        assert not unit.has_moved and unit.is_selected
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

    def get_attackable_squares(self):
        '''
        For this unit, get all attackable squares, taking into account its
        minimum and maximum range, as well as (s)COp boosts.
        Does not return empty tiles.

        Returns:
            - attackable_squares(set): each Tile that is attackable by
                                       self.selected_unit
        '''
        attackable_squares = set()
        unit = self.selected_unit
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
            self.defender_died(defender_tile)
            print("=== {}({}) killed {}".format(attacker, prev_a_health, defender))
        else:
            defense_damage = self.damage_formula(defender, attacker, attacker_tile.terrain)
            attacker.hp = max(0, round(attacker.hp - defense_damage, 1))
            attacker.visible_hp = math.ceil(attacker.hp/10)
            if attacker.hp == 0:
                self.attacker_died(attacker_tile)
                print("=== {} killed itself".format(attacker))
                return
            # print("=== {}({}) attacked {}({}) for {} vs {}".format(attacker, prev_a_health, defender, prev_d_health, round(attack_damage/10, 2), round(defense_damage/10, 2)))
        if attacker_tile.unit is not None: # Survived
            self.unready_unit(attacker_tile.unit)

    def damage_formula(self, attacker, defender, defender_terrain):
        first_term = (DAMAGE_CHART[attacker.type.value, defender.type.value] * 100) / 100 + random.randrange(0,10)
        second_term = attacker.visible_hp / 10
        third_term = (200 - (100 + defender_terrain.defense * defender.visible_hp)) / 100
        return first_term * second_term * third_term

    def create_unit(self, unit):
        assert self.battlefield[unit.x][unit.y].unit is None
        self.battlefield[unit.x][unit.y].unit = unit

    def attacker_died(self, tile):
        self.unselect_unit(tile.unit)
        tile.unit = None

    def defender_died(self, tile):
        tile.unit = None

    def select_unit(self, unit):
        assert self.selected_unit is None
        unit.is_selected = True
        self.selected_unit = unit
        # print("Selected {}".format(self.selected_unit))

    def unselect_unit(self, unit):
        assert self.selected_unit is not None
        unit.is_selected = False
        self.selected_unit = None
        self.selected_unit_moved = False

    def move_unit(self, unit, new_x, new_y):
        assert self.selected_unit is not None
        self.battlefield[unit.x][unit.y].unit = None
        self.battlefield[new_x][new_y].unit = unit
        old_x, old_y = unit.x, unit.y
        unit.x, unit.y = new_x, new_y
        unit.has_moved = True
        self.unit_moved = True
        # print("Moved {} from {} to {}".format(unit, (old_x, old_y), (new_x, new_y)))

    def unready_unit(self, unit):
        unit.unready()
        self.selected_unit = None
        self.selected_unit_moved = False
        # print("Finished handling ", unit)

    def end_turn(self):
        new_country = self.get_new_country()
        self.active_player = new_country
        self.start_turn()

    def start_turn(self):
        # print("========== NEW TURN: ", self.active_player, " =============")
        self.ready_country_units(self.active_player)
        self.selected_unit = None
        self.selected_unit_moved = False

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

    def check_turn_done(self):
        "TODO: bases, (s)COp etc"
        for row in range(len(self.battlefield)):
            for col in range(len(self.battlefield[row])):
                tile = self.battlefield[row][col]
                if tile.unit is None:
                    continue
                if tile.unit.country == self.active_player and not tile.unit.has_finished:
                    return False
        return True

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
