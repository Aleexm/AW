from enums import Movetype

class Unit():
    def __init__(self, country):
        self.country = country
        self.moved = False
        self.is_selected = False
        self.has_finished = False
        self.hp = 10

class Infantry(Unit):
    def __init__(self, country, x, y):
        super().__init__(country)
        self.fuel = 99
        self.ammo = 100
        self.x = x
        self.y = y
        self.encode_idx = 0
        self.movetype = Movetype.Foot
        self.movement = 3
        self.range = 1
        self.vision = 2
        self.cost = 1000

class Tank(Unit):
    "TODO FIX ENCODE IDX"
    def __init__(self, country, x, y):
        super().__init__(country)
        self.fuel = 70
        self.ammo = 9
        self.x = x
        self.y = y
        self.encode_idx = 1 # TODO FIX
        self.movetype = Movetype.Tire
        self.movement = 6
        self.range = 1
        self.vision = 3
        self.cost = 7000

class Recon(Unit):
    "TODO FIX ENCODE IDX"
    def __init__(self, country, x, y):
        super().__init__(country)
        self.fuel = 80
        self.ammo = 100
        self.x = x
        self.y = y
        self.encode_idx = 2 # TODO FIX
        self.movetype = Movetype.Wheels
        self.movement = 8
        self.range = 1
        self.vision = 5
        self.cost = 4000

    def __repr__(self):
        return '{} {} Infantry: {}HP {}Fuel {}Ammo'.format(str(self.x), str(self.y), self.hp, self.fuel, self.ammo)
