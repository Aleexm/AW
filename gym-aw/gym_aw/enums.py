import enum

class Weather(enum.Enum):
    Clear = 0
    Rain  = 1
    Snow  = 2

class Movetype(enum.Enum):
    Foot   = 0
    Mech   = 1
    Tire   = 2
    Wheels = 3
    Air    = 4
    Sea    = 5
    Lander = 6
    Pipe   = 7

class TerrainType(enum.Enum):
    Plain    = 0
    Mountain = 1
    Wood     = 2
    River    = 3
    Road     = 4
    Bridge   = 5
    Sea      = 6
    Shoal    = 7
    Reef     = 8
    Pipe     = 9
    Pipeseam = 10
    Rubble   = 11
    Missile  = 12
    City     = 13
    Base     = 14
    Airport  = 15
    Port     = 16
    HQ       = 17
    Comtower = 18
    Lab      = 19

class Country(enum.Enum):
    NoCountry       = -1
    Neutral         = 0
    OrangeStar      = 1
    BlueMoon        = 2
    GreenEarth      = 3
    YellowComet     = 4
    BlackHole       = 5
    RedFire         = 6
    GreySky         = 7
    BrownDesert     = 8
    AmberBlaze      = 9
    JadeSun         = 10
    CobaltIce       = 11
    PinkCosmos      = 12
    TealGalaxy      = 13
    PurpleLightning = 14
    AcidRain        = 15
    WhiteNova       = 16

class UnitType(enum.Enum):
    AntiAir         = 0
    APC             = 1
    Artillery       = 2
    BattleCopter    = 3
    Battleship      = 4
    BlackBoat       = 5
    BlackBomb       = 6
    Bomber          = 7
    Carrier         = 8
    Cruiser         = 9
    Fighter         = 10
    Infantry        = 11
    Lander          = 12
    MediumTank      = 13
    Mech            = 14
    MegaTank        = 15
    Missiles        = 16
    NeoTank         = 17
    Piperunner      = 18
    Recon           = 19
    Rockets         = 20
    Stealth         = 21
    Submarine       = 22
    TransportCopter = 23
    Tank            = 24
