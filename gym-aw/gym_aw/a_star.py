import heapq
from consts import *

def a_star(start, goal, battlefield, active_player, unit, weather, movement):
    '''
    Finds the shortest path between start and goal. If this distance is longer
    than the maximum movement of the unit, return None.

    Args:
        - start(Tile): Unit's starting location.
        - goal(Tile): Unit's goal (i.e. a square within its movement range)
        - battlefield(2D list of Tile): The battlefield
        - active_player(int): Enemy units are obstacles
        - unit(Unit): The unit to move
        - weather(Weather): Snow hinders movement etc
        - movement(int): The amount of tiles this unit can maximally move.

    Returns:
        - None: No path found within movement range from start to goal
        - Path(list(Tile)): The shortest path
    '''
    if traverse_tile_cost(goal, active_player, weather, unit) == MAX_TERRAIN_MOVE:
        return None, None

    # Only used for checking whether neighbor is still in the open_set.
    open_tiles = set()
    open_tiles.add(start)
    # This will contain (f_score, Tile) tuples, minheap datastructure for quickly
    # finding the Tile with minimum f_score
    open_set = list()
    came_from = dict() # Used for reconstructing the path
    g_score = dict() # Will contain distances from start to current node
    g_score[start] = 0
    f_score = dict() # f_score = g_score(start) + manhattan(current, goal)
    f_score[start] = manhattan(start, goal) # g_score(start) = 0
    heapq.heappush(open_set, (f_score[start], start)) # f_score is used to compare

    while len(open_set) > 0:
        current = heapq.heappop(open_set)[1] # [1] gives the Tile (not the f_score)
        open_tiles.remove(current)
        if current.x == goal.x and current.y == goal.y:
            return reconstruct_path(came_from, current, movement, active_player,
                                    weather, unit)
        if g_score[current] >= movement: # This square is unreachable
            continue

        for (add_x, add_y) in [(-1, 0), (0,1), (1,0), (0,-1)]: # NESW neighbor
            if current.x + add_x >= len(battlefield) \
            or current.y + add_y >= len(battlefield[0]):
                continue # Neighbor outside of map
            neighbor = battlefield[current.x + add_x][current.y + add_y] # Tile
            d_neighbor = traverse_tile_cost(neighbor, active_player, weather, unit)
            tentative_g_score = g_score[current] + d_neighbor
            if neighbor_has_better_g_score(tentative_g_score, g_score, neighbor):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan(neighbor, goal)
                if neighbor not in open_tiles:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_tiles.add(neighbor)

    return None, None

def reconstruct_path(came_from, current, movement, active_player, weather, unit):
    "Some wikipedia pseudocode magic. Returns both the path and the distance"
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    list.reverse(total_path)
    total_cost = 0
    for t in total_path[1:]:
        total_cost += traverse_tile_cost(t, active_player, weather, unit)
    return total_path, total_cost


def traverse_tile_cost(neighbor, active_player, weather, unit):
    "Returns distance based on unit's movement type, as well as the weather"
    if neighbor.unit is not None and neighbor.unit.country != active_player:
        return MAX_TERRAIN_MOVE # Enemy unit is blocking
    return neighbor.terrain.movement[weather][unit.movetype.value]

def manhattan(a, b):
    return abs(a.x-b.x) + abs(a.y-b.y)

def neighbor_has_better_g_score(tentative_g_score, g_score, neighbor):
    if neighbor not in g_score:
        return True
    else:
        if tentative_g_score < g_score[neighbor]:
            return True
        return False
