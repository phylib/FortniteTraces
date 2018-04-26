import random
import sys
import math
import numpy as np
import matplotlib.path as mplPath
from scipy import spatial
import processHeatmap

island_polygon_px = [(156, 49), (360, 50), (451, 113), (762, 100), (796, 80), (875, 97), (988, 440), (999, 529),
                     (941, 817), (790, 935), (494, 967), (306, 908), (292, 768), (101, 655), (26, 565), (20, 462),
                     (68, 197)]
island_polygon = np.array([[1.54455446, 0.48514851],
                           [3.56435644, 0.4950495],
                           [4.46534653, 1.11881188],
                           [7.54455446, 0.99009901],
                           [7.88118812, 0.79207921],
                           [8.66336634, 0.96039604],
                           [9.78217822, 4.35643564],
                           [9.89108911, 5.23762376],
                           [9.31683168, 8.08910891],
                           [7.82178218, 9.25742574],
                           [4.89108911, 9.57425743],
                           [3.02970297, 8.99009901],
                           [2.89108911, 7.6039604],
                           [1., 6.48514851],
                           [0.25742574, 5.59405941],
                           [0.1980198, 4.57425743],
                           [0.67326733, 1.95049505]])

poi_px = [(181, 102), (393, 153), (528, 213), (845, 283), (270, 284), (678, 313), (748, 405), (919, 685), (594, 455),
          (64, 446), (229, 483), (363, 465), (638, 536), (770, 539), (861, 492), (216, 621), (358, 641), (573, 613),
          (495, 714), (349, 755), (778, 745), (613, 770), (436, 831), (345, 889)]
poi = np.array([[0.17920792, 0.1009901],
                [0.38910891, 0.15148515],
                [0.52277228, 0.21089109],
                [0.83663366, 0.28019802],
                [0.26732673, 0.28118812],
                [0.67128713, 0.30990099],
                [0.74059406, 0.4009901],
                [0.90990099, 0.67821782],
                [0.58811881, 0.45049505],
                [0.06336634, 0.44158416],
                [0.22673267, 0.47821782],
                [0.35940594, 0.46039604],
                [0.63168317, 0.53069307],
                [0.76237624, 0.53366337],
                [0.85247525, 0.48712871],
                [0.21386139, 0.61485149],
                [0.35445545, 0.63465347],
                [0.56732673, 0.60693069],
                [0.49009901, 0.70693069],
                [0.34554455, 0.74752475],
                [0.77029703, 0.73762376],
                [0.60693069, 0.76237624],
                [0.43168317, 0.82277228],
                [0.34158416, 0.88019802]]) * 10

first_circle_radius = 10 * 0.65 / 2.
second_circle_radius = 10 * 0.32 / 2.
third_circle_radius = 10 * 0.1693 / 2.
forth_circle_radius = 10 * 0.079 / 2.
fifth_circle_radius = 10 * 0.0396 / 2.
sixth_circle_radius = 10 * 0.0198 / 2.

box_first_storm = (0.29, 9.708)

walk_speed = 1 / 45.
propability_to_rest = 0.2

time_first_storm = 90
time_second_storm = 480
time_third_storm = 715
time_forth_storm = 925
time_fifth_storm = 1105
time_sixth_storm = 1235

players_num = [(1, 97), (34, 96), (39, 95), (43, 94), (46, 93), (49, 92), (52, 91), (55, 90), (58, 89), (61, 88),
               (63, 87), (66, 86), (68, 85), (71, 84), (73, 83), (76, 82), (78, 81), (80, 80), (83, 79), (85, 78),
               (88, 77), (91, 76), (93, 75), (96, 74), (99, 73), (101, 72), (104, 71), (107, 70), (110, 69), (113, 68),
               (117, 67), (120, 66), (123, 65), (127, 64), (131, 63), (135, 62), (139, 61), (143, 60), (147, 59),
               (151, 58), (156, 57), (161, 56), (165, 55), (170, 54), (175, 53), (180, 52), (185, 51), (191, 50),
               (196, 49), (202, 48), (207, 47), (213, 46), (219, 45), (225, 44), (232, 43), (239, 42), (246, 41),
               (254, 40), (262, 39), (271, 38), (281, 37), (292, 36), (304, 35), (318, 34), (332, 33), (346, 32),
               (359, 31), (372, 30), (385, 29), (398, 28), (411, 27), (423, 26), (437, 25), (451, 24), (467, 23),
               (484, 22), (504, 21), (526, 20), (550, 19), (572, 18), (593, 17), (614, 16), (635, 15), (656, 14),
               (679, 13), (703, 12), (726, 11), (749, 10), (770, 9), (791, 8), (814, 7), (842, 6), (896, 5), (954, 4),
               (992, 3), (1287, 2), (1303, 1)]

propability_vector = None


def get_first_storm(box_boundaries=(box_first_storm[0], box_first_storm[1], box_first_storm[0], box_first_storm[1]),
                    radius=first_circle_radius):
    x = 0
    y = 0
    while not is_point_on_island((x, y)):
        x = random.random() * (box_boundaries[1] - box_boundaries[0]) + box_boundaries[0]
        y = random.random() * (box_boundaries[3] - box_boundaries[2]) + box_boundaries[2]
    return (x, y, radius)


def get_inner_storm(outer_storm, inner_storm_radius):
    outer_storm_boundary = outer_storm[2] - inner_storm_radius

    square = [outer_storm[0] - outer_storm_boundary, outer_storm[0] + outer_storm_boundary,
              outer_storm[1] - outer_storm_boundary, outer_storm[1] + outer_storm_boundary]

    x = 0
    y = 0

    while not is_in_circle((outer_storm[0], outer_storm[1], outer_storm_boundary), (x, y)) or not is_point_on_island(
            (x, y)):
        x = random.random() * (square[1] - square[0]) + square[0]
        y = random.random() * (square[3] - square[2]) + square[2]

    return (x, y, inner_storm_radius)


def is_in_circle(circle, point):
    # from https://stackoverflow.com/a/481150/2428434
    x = point[0]
    y = point[1]
    center_x = circle[0]
    center_y = circle[1]
    radius = circle[2]
    return math.pow(x - center_x, 2) + math.pow(y - center_y, 2) < math.pow(radius, 2)


def build_storm_map():
    first_circle = get_first_storm()
    storms = [first_circle]
    second_circle = get_inner_storm(first_circle, second_circle_radius)
    storms.append(second_circle)
    storms.append(get_inner_storm(storms[-1], third_circle_radius))
    storms.append(get_inner_storm(storms[-1], forth_circle_radius))
    storms.append(get_inner_storm(storms[-1], fifth_circle_radius))
    storms.append(get_inner_storm(storms[-1], sixth_circle_radius))
    return storms


def is_point_on_island(point):
    bbPath = mplPath.Path(island_polygon)
    return bbPath.contains_point(point)


def generate_player_trace(storms):

    global propability_vector
    if propability_vector is None:
        propability_vector = processHeatmap.process()

    poi_list = processHeatmap.read_pois()

    positions = []
    start_position = generate_start_point()
    time = 0
    positions.append((time, start_position, False))
    current_state = "rand"

    poi = None
    in_storm_boundary = random.random()*0.8 + 0.2
    while time < 1800:
        if time > time_first_storm:
            if current_state == "rand":
                poi_list = shrink_poi_list(poi_list, storms[0])
            current_state = 0
        if time > time_second_storm:
            if current_state == 0:
                poi_list = shrink_poi_list(poi_list, storms[1])
            current_state = 1
        if time > time_third_storm:
            if current_state == 1:
                poi_list = shrink_poi_list(poi_list, storms[3])
            current_state = 2
        if time > time_forth_storm:
            if current_state == 2:
                poi_list = shrink_poi_list(poi_list, storms[3])
            current_state = 3
        if time > time_fifth_storm:
            if current_state == 3:
                poi_list = shrink_poi_list(poi_list, storms[4])
            current_state = 4
        if time > time_sixth_storm:
            if current_state == 4:
                poi_list = shrink_poi_list(poi_list, storms[5])
            current_state = 5

        # if selected poi is in surrounding of 0.1 search for new poi
        if poi is None or is_in_circle((positions[-1][1][0], positions[-1][1][1], .05), poi):
            poi = None

        if current_state == "rand" and poi is None:
            poi = select_poi(positions[-1][1], poi_list)
        elif poi is None:
            poi = select_poi(positions[-1][1], poi_list, storms[current_state])

        if current_state == "rand":
            positions += walk(positions[-1][1], time, None, poi)
        else:
            positions += walk(positions[-1][1], time, storms[current_state], poi, in_storm_boundary=in_storm_boundary)
        time = positions[-1][0]

    return positions


def shrink_poi_list(poi_list, storm):
    new_poi_list = []
    for p in poi_list:
        if is_in_circle(storm, p):
            new_poi_list.append(p)

    return new_poi_list


def select_poi(position, poi_list, storm=None):
    p = None
    if len(poi_list) == 0:
        return p
    for i in range(0, 10):
        poi_index = random.randint(0, len(poi_list) - 1)
        p = poi_list[poi_index]
        if is_in_circle((position[0], position[1], 1), p):
            if storm is None:
                break
            elif is_in_circle(storm, p):
                break

    return p



def walk(position, time, target=None, poi = None, in_storm_boundary=0.8):
    walking_time = int(random.random() * 8 + 2)

    positions = []
    # resting?
    if random.random() < propability_to_rest:
        # rest
        for i in range(time + 1, time + 1 + walking_time):
            positions.append((i, position, False))
        return positions

    # if a storm exists, check if you are in storm
    if poi is not None and (target is None or is_in_circle((target[0], target[1], target[2] * in_storm_boundary), position)):
        target = (poi[0], poi[1], 0.1)

    # Walk
    if target is None or is_in_circle((target[0], target[1], target[2] * in_storm_boundary), position): # Random or in storm
        angle = int(random.random() * 360)
    else:
        theta = calc_angle(position, target)
        angle = int(random.random() * 80)
        angle += theta
        angle -= 40

    points = [((i + 1) * walk_speed, 0) for i in range(0, walking_time)]
    transformed_points = []
    for p in points:
        p_x = p[0] * math.cos(angle * math.pi / 180.) - p[1] * math.sin(angle * math.pi / 180.)
        p_y = p[1] * math.cos(angle * math.pi / 180.) + p[0] * math.sin(angle * math.pi / 180.)
        transformed_points.append((p_x, p_y))

    for p in transformed_points:
        time += 1
        positions.append((time, (position[0] + p[0], position[1] + p[1]), False))

    if not is_point_on_island(positions[-1][1]):
        return walk(position, time, target)

    return positions


def get_players_line(player_evolution):
    players = []
    current_num = 100
    player_dict = {}
    for (t, num) in player_evolution:
        player_dict[t] = num

    for time in range(0, player_evolution[-1][0]):
        if time in player_dict:
            current_num = player_dict[time]
        players.append((time, current_num))
    return players


def kill_players(player_logs, player_evolution):
    killed = set()
    kill_relations = {}

    for kill_log in player_evolution:
        players_to_kill = (len(player_logs) - len(killed)) - kill_log[1]

        for i in range(0, players_to_kill):

            positions = []
            kill_time = kill_log[0]
            for i in range(0, len(player_logs)):
                if i in killed:
                    continue
                positions.append((i, (player_logs[i][kill_time][1])))

            player_num, killer_num = find_closest_point(positions)

            #player_num = random.randint(0, len(player_logs) - 1)
            #while player_num in killed:
            #    player_num = random.randint(0, len(player_logs) - 1)

            player_logs[player_num] = player_logs[player_num][:kill_time]
            if len(player_logs[player_num]) > 0:
                player_logs[player_num][-1] = (player_logs[player_num][-1][0], player_logs[player_num][-1][1], True)
            killed.add(player_num)

            player_logs[killer_num][kill_time] = (player_logs[killer_num][kill_time][0],
                                                  player_logs[killer_num][kill_time][1],
                                                  True)
            kill_relations[player_num] = killer_num

    return (player_logs, kill_relations)


def find_closest_point(player_positions):
    positions = [(a[1][0], a[1][1]) for a in player_positions]

    min_distance = 100000
    min_idx_1 = -1
    min_idx_2 = -1
    second_point_coordinates = None

    for i in range(0, len(player_positions)):
        point = positions[i]
        others = positions[:i] + positions[i + 1:]
        distance, index = spatial.KDTree(others).query(point)
        if distance < min_distance:
            min_distance = distance
            min_idx_1 = player_positions[i][0]
            second_point_coordinates = others[index]

    for i in range(0, len(positions)):
        pos = player_positions[i]
        if pos[1][0] == second_point_coordinates[0] and pos[1][1] == second_point_coordinates[1]:
            min_idx_2 = pos[0]


    # print("Kill player {} (by player {}) with distance {}".format(min_idx_1, min_idx_2, min_distance))
    return min_idx_1, min_idx_2


def calc_angle(p1, p2):
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    return math.degrees(math.atan2(yDiff, xDiff))


def generate_start_point():
    global propability_vector

    x = 0
    y = 0
    while not is_point_on_island((x, y)):
        poi_index = random.randint(0, len(propability_vector) - 1)
        x,y = propability_vector[poi_index]
        x /= 150.
        y /= 150.
    return (x, y)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    else:
        seed = 0

    build_storm_map(seed)
