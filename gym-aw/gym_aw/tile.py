'''
===========================
These are the tiles that make up the final battlefield. They contain both a
Terrain class and a Unit class, as well as position etc.
===========================
'''

class Tile():
    def __init__(self, terrain, unit=None):
        self.terrain = terrain
        self.unit = unit
        self.x = self.terrain.x
        self.y = self.terrain.y

    def __repr__(self):
        return '{} {}'.format(str(self.terrain), str(self.unit))

    def __lt__(self, other):
        return self.x <= other.x
