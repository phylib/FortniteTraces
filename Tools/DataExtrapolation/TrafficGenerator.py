import numpy as np
import datetime
import os
import argparse
from FortnitePlotWorld import generate_player_traces
from FortnitePlotWorld import PlayerTrace
import logjoiner
import fnplog
import trafficstat

CLIENT_SPECTATOR = (19.359, 2.6462)
CLIENT_ACTIVE = (43.868, 7.9772)
SERVER_LOW = (81.572, 34.467)
SERVER_HIGH = (267.65, 57.955)


def create_packet_sizes(mu, sigma, n):
    s = np.random.normal(mu, sigma, n)
    return s


def create_packets_client_active(seconds, start_time):
    packet_sizes = []
    for s in range(0, seconds):
        num_packets = int(np.random.normal(35.937, 4.2692))
        inter_packet_dist = 1 / float(num_packets)
        sizes = create_packet_sizes(CLIENT_ACTIVE[0], CLIENT_ACTIVE[1], num_packets)
        for i in range(0, len(sizes)):
            packet_sizes = packet_sizes + [(start_time + s + i*inter_packet_dist, int(sizes[i]), "out")]

    return packet_sizes


def create_packets_client_spectator(seconds, start_time):
    packet_sizes = []
    for s in range(0, seconds):
        num_packets = int(np.random.normal(35.937, 4.2692))
        #num_packets = int(np.random.poisson(36.198))
        inter_packet_dist = 1 / float(num_packets)
        #sizes = np.random.poisson(20.228, num_packets)
        sizes = create_packet_sizes(CLIENT_SPECTATOR[0], CLIENT_SPECTATOR[1], num_packets)
        #sizes = np.random.binomial(4*20.228, 0.25, num_packets)
        #sizes = np.random.normal(20.228, 9.35, num_packets)
        for i in range(0, len(sizes)):
            packet_sizes = packet_sizes + [(start_time + s + i*inter_packet_dist, int(sizes[i]), "out")]

    return packet_sizes


def create_packets_server_low_action(seconds, start_time, server_packet_mean=19.731, server_packet_size_mean=SERVER_LOW[0], use_variation=False):
    packet_sizes = []
    variation = False
    next_variation = -1
    variation_time = 0
    for s in range(0, seconds):

        if next_variation < 0:
            next_variation = int(round(np.random.exponential(15, 1)))

        if next_variation == 0 and variation is False:
            variation = True
            variation_time = 0

        if variation or not use_variation:
            num_packets = int(np.random.normal(server_packet_mean, 1.6053))
            variation_time += 1
            if variation_time >= 3:
                variation = False
                next_variation = -1
        else:
            num_packets = server_packet_mean
            next_variation -= 1

        inter_packet_dist = 1 / float(num_packets)
        sizes = create_packet_sizes(server_packet_size_mean, SERVER_LOW[1], num_packets)
        for i in range(0, len(sizes)):
            packet_sizes = packet_sizes + [(start_time + s + i*inter_packet_dist, int(sizes[i]), "in")]

    return packet_sizes


def create_packets_server_high_action(seconds, start_time, server_packet_mean=19.731, server_packet_size_mean=SERVER_HIGH[0]):
    packet_sizes = []
    for s in range(0, seconds):
        num_packets = int(np.random.normal(server_packet_mean, 1.6053))
        inter_packet_dist = 1 / float(num_packets)
        sizes = create_packet_sizes(server_packet_size_mean, SERVER_HIGH[1], num_packets)
        for i in range(0, len(sizes)):
            packet_sizes = packet_sizes + [(start_time + s + i*inter_packet_dist, int(sizes[i]), "in")]

    return packet_sizes


def create_player_trace(player_movement_traces, selected_player):

    movement_trace = player_movement_traces.player_traces[selected_player]
    game_duration = player_movement_traces.no_players[-1][0]

    server_full_update_time = 0
    server_packet_higher_load = 0

    server_packet_higher_load_value = 550

    for (t, no_players) in player_movement_traces.no_players:
        if no_players < 80 and server_packet_higher_load == 0:
            server_packet_higher_load = t
        if no_players < 50:
            server_full_update_time = t
            break

    m = (20 - 10) / float(server_full_update_time - 0)

    m_server_packet_size = (SERVER_LOW[0] - server_packet_higher_load_value) / float(server_packet_higher_load - 0)

    playing_time = len(movement_trace)
    spectator_time = game_duration - playing_time
    client_packets = create_packets_client_active(playing_time, 0) + create_packets_client_spectator(spectator_time, playing_time)

    current_time = 0
    server_packets = []
    while current_time < game_duration:
        movement_trace = player_movement_traces.player_traces[selected_player][current_time:]
        action_times = [event[0] for event in filter(lambda c: c[2] == True, movement_trace)]

        generated_to = current_time

        for time in action_times:
            if generated_to < server_full_update_time or generated_to < server_packet_higher_load:

                for t in range(generated_to, time - 5):
                    if generated_to < server_full_update_time:
                        server_packet_freq_mean = m*generated_to + 10
                    else:
                        server_packet_freq_mean = 19.731

                    if generated_to < server_packet_higher_load:
                        server_packet_size_mean = m_server_packet_size*generated_to + server_packet_higher_load_value
                        server_packets = server_packets + create_packets_server_high_action(1, t, server_packet_freq_mean, server_packet_size_mean)
                    else:
                        server_packet_size_mean = SERVER_LOW[0]
                        server_packets = server_packets + create_packets_server_low_action(1, t, server_packet_freq_mean)
                    generated_to += 1
                for t in range(time - 5, time):
                    if generated_to < server_full_update_time:
                        server_packet_freq_mean = m*generated_to + 10
                    else:
                        server_packet_freq_mean = 19.731

                    if generated_to < server_packet_higher_load:
                        server_packet_size_mean = m_server_packet_size*generated_to + server_packet_higher_load_value
                    else:
                        server_packet_size_mean = SERVER_HIGH[0]
                    server_packets = server_packets + create_packets_server_high_action(1, generated_to, server_packet_freq_mean, server_packet_size_mean)
                    generated_to += 1

            else:
                seconds_to_generate = time - generated_to
                if seconds_to_generate > 5:
                    server_packets = server_packets + create_packets_server_low_action(seconds_to_generate - 5, generated_to, use_variation=True)
                server_packets = server_packets + create_packets_server_high_action(min(5, seconds_to_generate), generated_to + seconds_to_generate - min(5, seconds_to_generate))
                generated_to = time

        current_time = time
        if selected_player not in player_movement_traces.kill_relations:
            break
        selected_player = player_movement_traces.kill_relations[selected_player]

    return client_packets, server_packets


##
#  Start script for 100 player traces
#  > seq 0 99 | xargs -P 4 -I {} python /ndnSim/PythonScripts/fortnite/TrafficGenerator.py -p {} -o out
##

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--game", help="Trace is generated for the given game number", type=int, default=0)
parser.add_argument("-c", "--charts", help="Plot charts", type=bool, default=True)
parser.add_argument("-o", "--output", help="Output directory [./]", default="./")
parser.add_argument("-v", "--verbose", help="Show debug information", type=bool, default=False)
args = parser.parse_args()

game = args.game
plot = args.charts
verbose = args.verbose
output = args.output

if output[-1] != "/":
    output += "/"

if verbose:
    print("Generate movement traces")
player_movement_traces = generate_player_traces(game, verbose=verbose)
game_duration = player_movement_traces.no_players[-1][0]

if not os.path.exists(output):
    os.makedirs(output)
    
if verbose:
    print("Write movement traces")
for i in range(0, len(player_movement_traces.player_traces)):
    player_trace = player_movement_traces.player_traces[i]
    f = open(output + "player_{:02d}_movement.csv".format(i), "w")
    for entry in player_trace:
        f.write("{}\t{:10.3f}\t{:10.3f}\n".format(entry[0], entry[1][0], entry[1][1]))
    f.close()

for pl in range(0, 100):
    selected_player = pl
    if verbose:
        print("Generate traffic traces")
    client, server = create_player_trace(player_movement_traces, selected_player)

    packets = client + server
    packets.sort(key=lambda c:c[0])


    if verbose:
        print("Write Packet Log")
    f = open(output + "player_{:02d}_packet_log.csv".format(selected_player), "w")
    f.write("time\tin/out\tprotocol\tpayload-size\ttotal-size\n")

    for packet in packets:
        time = datetime.datetime.fromtimestamp(packet[0])
        time_str = time.strftime("%Y-%m-%d %H:%M:%S.%f")
        f.write("{}\t{}\t{}\t{}\t{}\n".format(time_str, packet[2], "udp:data", max(1, packet[1]), max(1, packet[1]) + 42))
    f.close()

    if verbose:
        print("Write game info")
    f = open(output + "player_{:02d}_game_info.csv".format(selected_player), "w")
    for i in range(0, game_duration):
        time = datetime.datetime.fromtimestamp(i)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        da = "alive"
        if i > len(player_movement_traces.player_traces[selected_player]):
            da = "dead"
        f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(time_str, i, i, player_movement_traces.no_players[i][1], "", da))
    f.close()

    if verbose:
        print("Calculate traffic averages")
    trafficstat.execute(output + "player_{:02d}_packet_log.csv".format(selected_player), output + "player_{:02d}_averages_packet_log.csv".format(selected_player))
    if verbose:
        print("Calculate combined logfile")
    logjoiner.execute(output + "player_{:02d}_averages_packet_log.csv".format(selected_player), output + "player_{:02d}_game_info.csv".format(selected_player), output + "player_{:02d}_joined.csv".format(selected_player))

    if plot:
        if verbose:
            print("Plot chart")
        fnplog.execute(output + "player_{:02d}_joined.csv".format(selected_player), output + "player_{:02d}.pdf".format(selected_player), verbose=verbose)