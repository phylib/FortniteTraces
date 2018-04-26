import os
import sys
import numpy as np
import argparse
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from pylab import rcParams
rcParams.update({'font.size': 11})

TARGET_FILE_POSTFIX = "_joined.csv"

def calcTrafficSums(inputDir, maxSpectatedSeconds):
    intervalDict = OrderedDict()
    # read content of neccessary files in inputDir
    for filename in sorted(os.listdir(inputDir)):
        if filename.endswith(TARGET_FILE_POSTFIX):
            print(filename)

            with open(os.path.join(inputDir, filename), 'r') as inputFile:
                spectatedSeconds = 0

                for row in inputFile.readlines():
                    # ['1970-01-01 01:04:45', '285', '285', '36', '', 'dead', '37', '19', '710', '1405', '19.00', '73.00\n']
                    parts = row.split('\t')

                    if spectatedSeconds >= maxSpectatedSeconds: break
                    if parts[5] != "alive":
                        spectatedSeconds += 1
                    #print(row.rstrip())

                    index = float(parts[1])
                    if index not in intervalDict:
                        intervalDict[index] = [0, 0]

                    intervalDict[index][0] += float(parts[8])
                    intervalDict[index][1] += float(parts[9])

    return intervalDict

def getPlayerCount(inputDir):
    intervalDict = OrderedDict()
    # read content of neccessary files in inputDir
    for filename in sorted(os.listdir(inputDir)):
        if filename.endswith(TARGET_FILE_POSTFIX):
            print(filename)
            with open(os.path.join(inputDir, filename), 'r') as inputFile:

                for row in inputFile.readlines():
                    # ['1970-01-01 01:04:45', '285', '285', '36', '', 'dead', '37', '19', '710', '1405', '19.00', '73.00\n']
                    parts = row.split('\t')
                    intervalDict[float(parts[1])] = int(parts[3])
                return intervalDict

def graph(intervalDict, outputFile):
    x = []
    outgoingMbps = []
    incomingMbps = []

    for timeIndex,values in intervalDict.iteritems():
        x.append(timeIndex)
        incomingMbps.append(values[0] * 0.000008)
        outgoingMbps.append(values[1] * 0.000008)

        # actually start drawing
    fig, ax = plt.subplots(figsize=(20, 8))

    ax.yaxis.grid('major')
    ax.plot(x, outgoingMbps, color='r', linestyle='-', label="outgoingMbps", zorder=0)
    ax.plot(x, incomingMbps, color='g', linestyle='-', label="outgoingMbps", zorder=0)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Bitrate [Mbps]')
    ax.tick_params('y')
    ax.set_xlim((0, x[-1]))

    plt.tight_layout()
    plt.savefig(outputFile, bbox_inches='tight')
    print(outputFile + " written")
    #plt.show()

def dualgraph(noQuittersDict, quittersDict, playerNumberDict, outputFile):
    x_no_quit = []
    x_quit = []
    x_players = []
    outgoingMbps_no_quit = []
    incomingMbps_no_quit = []
    outgoingMbps_quit = []
    incomingMbps_quit = []
    playerCount = []

    for timeIndex,values in noQuittersDict.iteritems():
        x_no_quit.append(timeIndex)
        incomingMbps_no_quit.append(values[0] * 0.000008)
        outgoingMbps_no_quit.append(values[1] * 0.000008)


    for timeIndex, values in quittersDict.iteritems():
        x_quit.append(timeIndex)
        incomingMbps_quit.append(values[0] * 0.000008)
        outgoingMbps_quit.append(values[1] * 0.000008)

    for timeIndex, cnt in playerNumberDict.iteritems():
        x_players.append(timeIndex)
        playerCount.append(cnt)

        # actually start drawing
    fig, ax = plt.subplots(figsize=(15, 4))

    ax.yaxis.grid('major')
    ax.plot(x_quit, outgoingMbps_quit, color='r', linestyle='-', label="Outgoing Traffic (without spectators)", zorder=0)
    ax.plot(x_quit, incomingMbps_quit, color='g', linestyle='-', label="Incoming Traffic (without spectators)", zorder=0)
    ax.plot(x_no_quit, outgoingMbps_no_quit, color='r', linestyle='--', dashes=(2, 2), label="Outgoing Traffic (including spectators)", zorder=0)
    ax.plot(x_no_quit, incomingMbps_no_quit, color='g', linestyle='--', dashes=(2, 2), label="Incoming Traffic (including spectators)", zorder=0)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Bitrate [Mbps]')
    ax.tick_params('y')
    ax.set_xlim((0, x_no_quit[-1]))

    ax2 = ax.twinx()
    ax2.plot(x_players, playerCount, color='#3284AD', linestyle='-', label="Active Players", zorder=0)
    ax2.set_xlim((0, x_no_quit[-1]))
    ax.plot(np.nan, color='#3284AD', linestyle='-', label="Active Players")  # just adding a line to legend
    ax2.set_ylabel('No. of Active Players')

    ax.legend(loc='upper center', bbox_to_anchor=(0.415, 1.02))
    ax.set_title("Traffic Load on Game Server")

    plt.tight_layout()
    plt.savefig(outputFile, bbox_inches='tight')
    print(outputFile + " written")
    #plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputDir")
    parser.add_argument("-s", "--maxSpectatedSeconds")
    parser.add_argument("-o", "--outputFile")
    args = parser.parse_args()

    traffic_no_quitters = calcTrafficSums(args.inputDir, sys.maxint)
    traffic_quit_after_n = calcTrafficSums(args.inputDir, int(args.maxSpectatedSeconds))

    playerNumberCurve = getPlayerCount(args.inputDir)

    #graph(traffic_no_quitters, args.outputFile)
    dualgraph(traffic_no_quitters, traffic_quit_after_n, playerNumberCurve, args.outputFile)