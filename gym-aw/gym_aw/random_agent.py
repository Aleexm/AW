import random
import numpy as np

class RandomAgent():
    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return "RandomAgent"

    def act(self, env):
        nonzero_actionable_units = np.nonzero(env.get_actionable_units())
        nonzero_row = nonzero_actionable_units[0]
        nonzero_col = nonzero_actionable_units[1]
        for row, col in zip(nonzero_row, nonzero_col):
            unit = env.battlefield[row][col].unit
            env.select_unit(unit)
            # movable_squares = env.get_reachable_squares(unit)
            # new_square = random.choice(tuple(movable_squares))
            # old_x, old_y = unit.x, unit.y
            # env.move_unit(unit, new_square.x, new_square.y)
            # print("Moved {} from {} to {}".format(str(unit), (old_x, old_y), (new_square.x, new_square.y)))
            attackable_squares = env.get_attackable_squares(unit)
            if len(attackable_squares) > 0:
                attacked_tile = random.choice(tuple(attackable_squares))
                env.attack_unit(env.battlefield[row][col], attacked_tile)
