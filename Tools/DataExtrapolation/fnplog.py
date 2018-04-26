import os
import argparse
import sys
import numpy as np
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.font_manager import FontProperties


# expected input-file-format
# index:   <0>                <1>         <2>               <3>             <4>              <5>                <6>            <7>           <8>                 <9>                <10>                 <11>
#    # abs-time #           #nr#      #game-time#    #alive-players#    #game-state#    #player-state#     #client-msg#	  #server-msg#	#client-bytes#	   #server-bytes#	 #avg-client-bytes#	  #avg-server-bytes#
# 2018-02-08 17:05:35       0019         -001             79               storm            alive               20             7             660               2887                33.00               412.43


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1 - y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny + dy, maxy + dy)


def execute(input, output_file, verbose=False):
    abs_time_points = []
    nr = []
    nr_for_alive_players = []
    game_time = []
    alive_players = []
    game_states = []
    player_states = []
    client_msg_cnt = []
    server_msg_cnt = []
    client_bytes = []
    server_bytes = []
    client_bytes_avg = []
    server_bytes_avg = []

    player_alive = []
    player_dead = []

    # read all available data
    with open(input, "r") as input_file:
        for line in input_file.readlines()[1:]:
            parts = line.rstrip().split('\t')  # see expected input-file format

            # general game properties
            abs_time_points.append(datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S'))
            nr.append(int(parts[2]))
            game_time.append(int(parts[2]) if parts[2] != '' else 0)  # not always present (default-value?)

            if parts[3] != '':  # not always present
                nr_for_alive_players.append(int(parts[2]))
                alive_players.append(int(parts[3]))

            game_states.append(parts[4])
            player_states.append(parts[5])

            # traffic properties (not always present)
            argc = len(parts)
            client_msg_cnt.append(int(parts[6]) if argc > 6 else 0)
            server_msg_cnt.append(int(parts[7]) if argc > 7 else 0)
            client_bytes.append(int(parts[8]) if argc > 8 else 0)
            server_bytes.append(int(parts[9]) if argc > 9 else 0)
            client_bytes_avg.append(float(parts[10]) if argc > 10 else 0.0)
            server_bytes_avg.append(float(parts[11]) if argc > 11 else 0.0)

    # additional processing / smoothing of data
    stages = []  # init
    stage_endtimes = []
    current_stage = ''  # init

    for index, game_state in enumerate(game_states):
        if game_state == '': continue

        if game_state != current_stage:
            stage_endtimes.append(nr[index])
            stages.append(current_stage)
            current_stage = game_state

    # search from back to find end of last segment
    for index, game_state in enumerate(reversed(game_states)):
        if game_state == current_stage:
            stage_endtimes.append(nr[-1] - index)
            stages.append(current_stage)
            break

    if verbose:
        print(stages)
        print(stage_endtimes)

    # actually start drawing
    fig = plt.figure(figsize=(20, 7))
    ax1 = fig.add_subplot(1, 1, 1)
    fig.canvas.set_window_title(input.split("/")[-1])
    # ax1.set_title("")

    fontP = FontProperties()
    fontP.set_size("14")

    ax1.yaxis.grid('major')
    ax1.plot(nr, client_bytes_avg, color='orange', linestyle='-', label="Avg. Outgoing Payload Size", zorder=0)
    ax1.plot(nr, server_bytes_avg, color='purple', linestyle='-', label="Avg. Incoming Payload Size", zorder=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Payload Size [bytes]')
    ax1.tick_params('y')
    ax1.set_xlim((0, nr[-1]))

    ax2 = ax1.twinx()
    ax2.plot(nr, client_msg_cnt, 'r', label="No of Outgoing Pkts/s")
    ax2.plot(nr, server_msg_cnt, 'g', label="No of Incoming Pkts/s")
    ax2.plot(nr_for_alive_players, alive_players, 'b', label="Active Players", zorder=20)
    ax2.yaxis.grid('major')
    ax2.set_xlim((0, nr[-1]))
    ax2.set_ylim((0, 100))

    # find the players end-of-life
    try:
        time_of_death = nr[player_states.index("dead")]
        ax2.axvline(time_of_death, color='k', linestyle="--", label="End of Active Play")
        ax2.barh(-2, nr[-1], 3, color='r')
        ax2.barh(-2, time_of_death, 3, color='g')
    except ValueError:
        pass

    stagebar_width = 1
    y_coord = 1
    reversed_stage_endtimes = list(reversed(stage_endtimes))
    for index, stage in enumerate(reversed(stages)):
        if verbose:
            print("drawing: " + stage + ", ends at: " + str(reversed_stage_endtimes[index]))
        if stage == 'storm':
            ax2.barh(y_coord, reversed_stage_endtimes[index], stagebar_width, color='purple', edgecolor='black',
                     label="Storm Phase")
        elif stage == 'move':
            ax2.barh(y_coord, reversed_stage_endtimes[index], stagebar_width, color='violet', edgecolor='black',
                     label="Contraction Phase", hatch='//')
        elif stage == 'jump':
            ax2.barh(y_coord, reversed_stage_endtimes[index], stagebar_width, color='blue', edgecolor='black',
                     label="Jump Phase")
        elif stage == 'bus':
            ax2.barh(y_coord, reversed_stage_endtimes[index], stagebar_width, color='blue', edgecolor='black',
                     label=stage)
        #elif stage == '':
        #    ax2.barh(y_coord, reversed_stage_endtimes[index], stagebar_width, color='white', edgecolor='black',
        #             label=stage)
    if verbose:
        print("done drawing stages.")

    # Make the y-axis label, ticks and tick labels match the line color.
    ax2.set_ylabel('No. of Players/Packets')

    ax2.plot(np.nan, color='orange', linestyle='-', label="Avg. Payload Size (Outgoing)")  # just adding a line to legend
    ax2.plot(np.nan, color='purple', linestyle='-', label="Avg. Payload Size (Incoming)")  # just adding a line to legend

    m1, = ax2.plot([], [], c='green', marker='s', markersize=15,
                  fillstyle='left', linestyle='none')

    m2, = ax2.plot([], [], c='red', marker='s', markersize=15,
                  fillstyle='right', linestyle='none')

    # ax2.legend(loc='upper right')

    handles, labels = plt.gca().get_legend_handles_labels()
    handles.append((m1,m2))
    labels.append("Active Player / Spectator")
    by_label = OrderedDict(zip(labels, handles))
    ax2.legend(by_label.values(), by_label.keys(), loc='upper right', numpoints=1)

    ax2.axhline(0, color='k')

    align_yaxis(ax1, 0, ax2, 0)
    plt.tight_layout()

    # fig_name = "".join(input_file.split(".")[:-1]).replace(".", "").replace("/", "") + ".pdf"
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    # plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    parser.add_argument("-v", "--verbose", help="Show debug information", type=bool, default=False)
    args = parser.parse_args()

    input = args.input
    output = args.output
    verbose = args.verbose

    execute(input, output, verbose)
