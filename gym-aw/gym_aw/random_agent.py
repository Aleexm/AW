import random
import numpy as np

class RandomAgent():
    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return "RandomAgent"

    # def act(self, env):
    #     nonzero_actionable_units = np.nonzero(env.get_actionable_units())
    #     nonzero_row = nonzero_actionable_units[0]
    #     nonzero_col = nonzero_actionable_units[1]
    #     for row, col in zip(nonzero_row, nonzero_col):
    #         unit = env.battlefield[row][col].unit
    #         env.select_unit(unit)
    #         movable_squares = env.get_reachable_squares(unit)
    #         new_square = random.choice(tuple(movable_squares))
    #         old_x, old_y = unit.x, unit.y
    #         env.move_unit(unit, new_square.x, new_square.y)
    #         print("Moved {} from {} to {}".format(str(unit), (old_y, old_x), (new_square.y, new_square.x)))
    #         attackable_squares = env.get_attackable_squares(unit)
    #         if len(attackable_squares) > 0:
    #             print(attackable_squares)
    #             attacked_tile = random.choice(tuple(attackable_squares))
    #             env.attack_unit(env.battlefield[unit.x][unit.y], attacked_tile)
    #         env.unselect_unit(unit)
    #         unit.unready()

    def act(self, env):
        valid_actions = env.get_valid_actions().flatten()
        valid_idx = np.nonzero(valid_actions)[0]
        if len(valid_idx) == 0:
            print(env)
        action = random.choice(valid_idx)
        return action
