import heapq


def a_star(start, goal, battlefield, active_player, unit, weather, movement):
    open_tiles = dict()
    open_set = list()
    open_tiles[start] = True
    came_from = dict()
    g_score = dict()
    g_score[start] = 0
    f_score = dict()
    f_score[start] = manhattan(start, goal)
    heapq.heappush(open_set, (f_score[start], start))

    while len(open_set) > 0:
        current = heapq.heappop(open_set)[1]
        del open_tiles[current]
        if current.x == goal.x and current.y == goal.y:
            return reconstruct_path(came_from, current, movement)
        if g_score[current] >= movement:
            continue

        for (add_x, add_y) in [(-1, 0), (0,1), (1,0), (0,-1)]: # NESW neighbor
            if current.x+add_x >= len(battlefield) \
            or current.y+add_y >= len(battlefield[0]):
                continue
            neighbor = battlefield[current.x+add_x][current.y+add_y]
            d_neighbor = get_distance_to_neighbor(neighbor, active_player, weather, unit)
            # print(current.x, current.y, ' ', neighbor.x, neighbor.y, ' ', d_neighbor)
            tentative_g_score = g_score[current] + d_neighbor
            if neighbor_has_better_g_score(tentative_g_score, g_score, neighbor):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan(neighbor, goal)
                if neighbor not in open_tiles:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_tiles[neighbor] = True

    return None

def reconstruct_path(came_from, current, movement):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    list.reverse(total_path)
    return total_path


def get_distance_to_neighbor(neighbor, active_player, weather, unit):
    if neighbor.unit is not None and neighbor.unit.country != active_player:
        return 100
    return neighbor.terrain.movement[weather][unit.movetype.value]

def manhattan(a, b):
    return abs(a.x-b.x) + abs(a.y-b.y)

def neighbor_has_better_g_score(tentative_g_score, g_score, neighbor):
    if neighbor not in g_score:
        return True
    else:
        if tentative_g_score < g_score[neighbor]:
            return True
