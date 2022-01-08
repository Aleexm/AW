from gym_aw.dicts import TERRAIN_DICT
from gym_aw.consts import *
from gym_aw.enums import *
import enum

class Terrain():
    def __init__(self, x, y, country):
        self.x = x
        self.y = y
        self.country = country
        self.is_property = country.value >= 0
        if self.is_property:
            self.capture_points = 20
        else:
            self.capture_points = -1

    def capture(self, cpt, country):
        self.capture_points = max(0, self.capture_points-cpt)
        if self.capture_points == 0:
            self.change_owner(country)

    def reset_capture(self):
        self.capture_points = 20

    def change_owner(self, country):
        self.country = country
        self.reset_capture()
    #
    # def set_type(self):
    #     "Remaps AWBW ids to actual terrain Types"
    #     if self.id == 1:
    #         self.type = Plain()
    #     elif self.id == 2:
    #         self.type = Mountain()
    #     elif self.id == 3:
    #         self.type = Wood()
    #     elif self.id in list(range(4,15)):
    #         self.type = River()
    #     elif self.id in list(range(15,26)):
    #         self.type = Road()
    #     elif self.id in [26, 27]:
    #         self.type = Bridge()
    #     elif self.id == 28:
    #         self.type = Sea()
    #     elif self.id in list(range(29,33)):
    #         self.type = Shoal()
    #     elif self.id == 33:
    #         self.type = Reef()
    #     elif self.id in [34, 38, 43, 48, 53, 81, 86, 91, 96, 119, 124, 151, 158, 165, 172, 183, 190]:
    #         self.type = City()
    #     elif self.id in [35, 39, 44, 49, 54, 82, 87, 92, 97, 118, 123, 150, 157, 164, 171, 182, 189]:
    #         self.type = Base()
    #     elif self.id in [36, 40, 45, 50, 55, 83, 88, 93, 98, 117, 122, 149, 156, 163, 170, 181, 188]:
    #         self.type = Airport()
    #     elif self.id in [37, 41, 46, 51, 56, 84, 89, 94, 99, 121, 126, 155, 162, 169, 176, 187, 194]:
    #         self.type = Port()
    #     elif self.id in [127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 152, 159, 166, 173, 184, 191]:
    #         self.type = Comtower()
    #     elif self.id in [138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 154, 161, 168, 175, 186, 193]:
    #         self.type = Lab()
    #     elif self.id in [42, 47, 52, 57, 85, 90, 95, 100, 120, 125, 153, 160, 167, 174, 185, 192]:
    #         self.type = HQ()
    #     elif self.id in list(range(101, 111)):
    #         self.type = Pipe()
    #     elif self.id in [113, 114]:
    #         self.type = Pipeseam()
    #     elif self.id in [115, 116]:
    #         self.type = Rubble()
    #     elif self.id in [111, 112]:
    #         self.type = Missile()
    #
    # def set_country(self):
    #     "see https://awbw.amarriner.com/countries.php"
    #     if self.id in [34,35,36,37,133,145]: #Neutral
    #         self.country = 0
    #     elif self.id in [38,39,40,41,42,134,146]: #OS
    #         self.country = 1
    #     elif self.id in [43,44,45,46,47,129,140]: #BM etc
    #         self.country = 2
    #     elif self.id in [48,49,50,51,52,131,142]:
    #         self.country = 3
    #     elif self.id in [53,54,55,56,57,136,148]:
    #         self.country = 4
    #     elif self.id in [91,92,93,94,95,128,139]:
    #         self.country = 5
    #     elif self.id in [81,82,83,84,85,135,147]:
    #         self.country = 6
    #     elif self.id in [86,87,88,89,90,137,143]:
    #         self.country = 7
    #     elif self.id in [96,97,98,99,100,130,141]:
    #         self.country = 8
    #     elif self.id in [117,118,119,120,121,127,138]:
    #         self.country = 9
    #     elif self.id in [122,123,124,125,126,132,144]:
    #         self.country = 10
    #     elif self.id in [149,150,151,152,153,154,155]:
    #         self.country = 11
    #     elif self.id in [156,157,158,159,160,161,162]:
    #         self.country = 12
    #     elif self.id in [163,164,165,166,167,168,169]:
    #         self.country = 13
    #     elif self.id in [170,171,172,173,174,175,176]:
    #         self.country = 14
    #     elif self.id in [181,182,183,184,185,186,187]:
    #         self.country = 15
    #     elif self.id in [188,189,190,191,192,193,194]:
    #         self.country = 16
    #     else:
    #         self.country = -1 # Just a terrain tile, no country


    def __repr__(self):
        x_str = str(self.x)
        if len(x_str) == 1:
            x_str += ' '
        y_str = str(self.y)
        if len(y_str) == 1:
            y_str += ' '
        type_str = str(self.type)
        for i in range(8-len(type_str)):
            type_str += ' '
        cpt_string = str(self.capture_points)
        if len(cpt_string) == 1:
            cpt_string += ' '
        country_string = str(self.country)
        for i in range(2-(len(country_string))):
            country_string += ' '
        return '{} {} {} p: {}, c: {}'.format(x_str, y_str, type_str,
                                              country_string, cpt_string)

class Plain(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 1
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,2 ,3 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [2 ,1 ,2 ,3 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 0

    def __repr__(self):
        return 'plain'

class Mountain(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 4
        self.movement = {
            Weather.Clear : [2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [4 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 1

    def __repr__(self):
        return 'Mountain'

class Wood(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 2
        self.movement = {
            Weather.Clear : [1 ,1 ,2 ,3 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,3 ,4 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [2 ,1 ,2 ,3 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 2

    def __repr__(self):
        return 'Wood'

class River(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 3

    def __repr__(self):
        return 'River'

class Road(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 4

    def __repr__(self):
        return 'Road'

class Bridge(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 5

    def __repr__(self):
        return 'Bridge'

class Sea(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,1 ,1 ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,1 ,1 ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,2 ,2 ,2 ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 6

    def __repr__(self):
        return 'Sea'

class Shoal(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,1 ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 7

    def __repr__(self):
        return 'Shoal'

class Reef(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 1
        self.movement = {
            Weather.Clear : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,2 ,2 ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1 ,2 ,2 ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,2 ,2 ,2 ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 8

    def __repr__(self):
        return 'Reef'


class Pipe(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1],
            Weather.Rain  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1],
            Weather.Snow  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1]
        }
        self.encode_idx = 9

    def __repr__(self):
        return 'Pipe'

class Pipeseam(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 0
        self.movement = {
            Weather.Clear : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1],
            Weather.Rain  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1],
            Weather.Snow  : [MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1]
        }
        self.encode_idx = 10

    def __repr__(self):
        return 'Pipeseam'

class Rubble(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 1
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,2 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,2 ,3 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [2 ,1 ,2 ,3 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 11

    def __repr__(self):
        return 'Rubble'

class Missile(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 12

    def __repr__(self):
        return 'Missile'

class City(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 13

    def __repr__(self):
        return 'City'

class Base(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,1]
        }
        self.encode_idx = 14

    def __repr__(self):
        return 'Base'

class Airport(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 15

    def __repr__(self):
        return 'Airport'

class Port(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,2 ,2 ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 16

    def __repr__(self):
        return 'Port'

class HQ(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 4
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 17

    def __repr__(self):
        return 'HQ'

class Comtower(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 18

    def __repr__(self):
        return 'Comtower'

class Lab(Terrain):
    def __init__(self, x, y, country):
        super().__init__(x, y, country)
        self.defense = 3
        self.movement = {
            Weather.Clear : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Rain  : [1 ,1 ,1 ,1 ,1 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE],
            Weather.Snow  : [1 ,1 ,1 ,1 ,2 ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE ,MAX_TERRAIN_MOVE]
        }
        self.encode_idx = 19

    def __repr__(self):
        return 'Lab'
