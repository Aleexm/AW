import enum

class Weather(enum.Enum):
    Clear = 0
    Rain = 1
    Snow = 2

class Movetype(enum.Enum):
    Foot = 0
    Mech = 1
    Tire = 2
    Wheels = 3
    Air = 4
    Sea = 5
    Lander = 6
    Pipe = 7
