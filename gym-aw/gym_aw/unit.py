from enums import Movetype, UnitType

class Unit():
    def __init__(self, country):
        self.country = country
        self.moved = False
        self.is_selected = False
        self.has_moved = False
        self.has_finished = False
        self.hp = 100
        self.visible_hp = 10

    def ready(self):
        self.fuel = max(0, self.fuel - self.upkeep_fuel)
        self.is_selected = False
        self.has_moved = False
        self.has_finished = False

    def unready(self):
        self.is_selected = False
        self.has_moved = True
        self.has_finished = True

    def __repr__(self):
        return '{} x{} y{}'.format(type(self), self.x, self.y)

class Infantry(Unit):
    def __init__(self, country, x, y):
        super().__init__(country)
        self.type = UnitType.Infantry
        self.fuel = 99
        self.upkeep_fuel = 0
        self.ammo = 100
        self.x = x
        self.y = y
        self.encode_idx = 0
        self.movetype = Movetype.Foot
        self.movement = 3
        self.min_range = 1
        self.max_range = 1
        self.vision = 2
        self.cost = 1000

class Tank(Unit):
    "TODO FIX ENCODE IDX"
    def __init__(self, country, x, y):
        super().__init__(country)
        self.type = UnitType.Tank
        self.fuel = 70
        self.upkeep_fuel = 0
        self.ammo = 9
        self.x = x
        self.y = y
        self.encode_idx = 1 # TODO FIX
        self.movetype = Movetype.Tire
        self.movement = 6
        self.min_range = 1
        self.max_range = 1
        self.vision = 3
        self.cost = 7000

class Recon(Unit):
    "TODO FIX ENCODE IDX"
    def __init__(self, country, x, y):
        super().__init__(country)
        self.type = UnitType.Recon
        self.fuel = 80
        self.upkeep_fuel = 0
        self.ammo = 100
        self.x = x
        self.y = y
        self.encode_idx = 2 # TODO FIX
        self.movetype = Movetype.Wheels
        self.movement = 8
        self.min_range = 1
        self.max_range = 1
        self.vision = 5
        self.cost = 4000
