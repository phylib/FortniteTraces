import numpy as np
import random

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import scipy

import FortniteWorldGeneration

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


class PlayerTrace:

    def __init__(self, player_traces, no_players, kill_relations):
        self.player_traces = player_traces
        self.no_players = no_players
        self.kill_relations = kill_relations


def generate_player_evolution():
    exp_x = np.append(scipy.random.exponential(15, 3), scipy.random.exponential(3, 27))
    exp_x = np.append(exp_x, scipy.random.exponential(5, 31))
    exp_x = np.append(exp_x, scipy.random.exponential(10, 10))
    exp_x = np.append(exp_x, scipy.random.exponential(18, 20))
    exp_x = np.append(exp_x, scipy.random.exponential(30, 5))
    exp_x = np.append(exp_x, scipy.random.exponential(120, 4))
    exp_y = range(1, 101)
    exp_y.reverse()
    exp_x = np.cumsum(exp_x)
    exp_x = [int(round(_)) for _ in exp_x]

    player_tuples = []
    for i in range(0, len(exp_y)):
        player_tuples.append((exp_x[i], exp_y[i]))
    return player_tuples


def generate_player_traces(game, verbose=False):
    # Build same map for all players
    random.seed(game * 1000)
    np.random.seed(game * 1000)
    storms = FortniteWorldGeneration.build_storm_map()

    #random.seed(game * 1000)
    #np.random.seed(game * 1000)

    player_evolution = generate_player_evolution()

    player = []
    for i in range(0, 100):
        player.append(FortniteWorldGeneration.generate_player_trace(storms))
        if verbose:
            print("generated trace for player " + str(i))

    player, kill_relations = FortniteWorldGeneration.kill_players(player, player_evolution)

    traces = PlayerTrace(player, FortniteWorldGeneration.get_players_line(player_evolution), kill_relations)
    return traces


if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(20, 20))
    patches = []

    polygon = Polygon(island_polygon, True)
    patches.append(polygon)

    #storms = FortniteWorldGeneration.build_storm_map(21)
    # storms = 10 * np.array(storms)
    #for storm in storms:
    #    patches.append(Circle((storm[0], storm[1]), storm[2]))

    player = generate_player_traces(3, verbose=True)

    for pl in player.player_traces:
        for pos in pl:
            patches.append(Circle((pos[1][0], pos[1][1]), 0.01))

    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)

    # colors = 100*np.random.rand(len(patches))
    # p.set_array(np.array(colors))

    ax.add_collection(p)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    plt.savefig("test.png")
    plt.close()

    for i in range(0, len(player.player_traces)):
        player_trace = player.player_traces[i]
        f = open("movements/movement_p" + str(i) + ".csv", "w")
        for entry in player_trace:
            f.write("{}\t{}\t{}\n".format(entry[0], round(entry[1][0]*150), round(entry[1][1]*150)))
        f.close()