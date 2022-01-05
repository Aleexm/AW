class Unit():
    def __init__(self, country):
        self.country = country
        self.moved = False
        self.is_selected = False

class Infantry(Unit):
    def __init__(self, country, x, y):
        super().__init__(country)
        self.hp = 10
        self.fuel = 99
        self.ammo = 100
        self.x = x
        self.y = y
        self.encode_idx = 0

    def __repr__(self):
        return '{} {} Infantry: {}HP {}Fuel {}Ammo'.format(str(self.x), str(self.y), self.hp, self.fuel, self.ammo)
