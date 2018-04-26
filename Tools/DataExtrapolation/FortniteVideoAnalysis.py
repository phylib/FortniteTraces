import sys
import glob
import time
import datetime
import re
import cv2
import numpy as np

storm = None
move = None
jump = None
bus = None


def analyze_folder(folder):
    if folder[-1] != "/":
        folder += "/"
    log_files = glob.glob(folder + "*.txt")
    log_files.sort()

    first = get_no_from_name(log_files[0])
    last = get_no_from_name(log_files[-1])

    date_re = re.compile('\d{2}:\d{2}:\d{2}')

    folder_re = re.compile('g\d{1,2}')
    game = ""
    if folder_re.match(folder):
        game = "_" + folder_re.search(folder).group(0)

    d_a = "alive"
    old_state = None
    game_start = None
    logs = []
    for num in range(int(first), int(last) + 1):


        # Read Timestamp
        f = open(folder + "timestamp_" + str(num).zfill(4) + ".png_prep.png.txt")
        timestamp = f.readlines()
        if len(timestamp) < 1:
            continue
        timestamp = timestamp[0].strip()
        timestamp = timestamp.replace(" ", "")
        if not date_re.match(timestamp):
            continue
        t = datetime.datetime.strptime("2018-02-08 " + timestamp, "%Y-%m-%d %H:%M:%S")
        f.close()

        # Read numplayesr
        f = open(folder + "players_" + str(num).zfill(4) + ".png_prep.png.txt")
        num_players = f.readlines()
        f.close()
        if len(num_players) < 1:
            num_players = ""
        else:
            num_players = num_players[0].strip()
        if not num_players.isdigit() or int(num_players) < 0 or int(num_players) > 100:
            num_players = ""

        # Read num_players when dead
        if num_players is "":
            f = open(folder + "players_dead_" + str(num).zfill(4) + ".png_prep.png.txt")
            num_players = f.readlines()
            f.close()
            if len(num_players) < 1:
                num_players = ""
            else:
                num_players = num_players[0].strip()
            if not num_players.isdigit() or int(num_players) < 0 or int(num_players) > 100:
                num_players = ""
            else:
                d_a = "dead"

        # Read State
        state = get_game_state(folder, num, d_a, num_players)

        if game_start is None and state == "jump" and old_state == "bus":
            game_start = num

        game_time = -1
        if game_start is not None:
            game_time = num - game_start

        # print as CSV
        logs.append(t.strftime("%Y-%m-%d %H:%M:%S") + "\t" + str(num).zfill(4) + "\t" + str(game_time).zfill(4) + "\t" + num_players + "\t" + state + "\t" + d_a)
        old_state = state

    logs.sort()
    f = open(folder + "extracted" + game + ".log", "w")
    for log in logs:
        f.write(log + "\n")
    f.close()


def get_game_state(folder, num, d_a, players):
    global storm
    global move
    global jump
    global bus

    if d_a == "alive":
        state_icon =  cv2.imread(folder + "storm_" + str(num).zfill(4) + ".png_prep.png")
    else:
        if players.isdigit() and int(players) < 10:
            state_icon = cv2.imread(folder + "dead_end_prep/storm_dead_end_" + str(num).zfill(4) + ".png_prep.png")
        else:
            state_icon = cv2.imread(folder + "storm_dead_" + str(num).zfill(4) + ".png_prep.png")
    #state_icon = cv2.cvtColor(state_icon, cv2.COLOR_BGR2GRAY)
    state = "storm"
    er = mse(state_icon, storm)
    if mse(state_icon, move) < er:
        state = "move"
        er = mse(state_icon, move)
    if mse(state_icon, jump) < er:
        state = "jump"
        er = mse(state_icon, jump)
    if mse(state_icon, bus) < er:
        state = "bus"
        er = mse(state_icon, bus)

    if er > 10000:
        return ""
    return state

def read_sample_images():
    global storm
    global move
    global jump
    global bus

    storm = cv2.imread("samples/storm.png")
    move = cv2.imread("samples/move.png")
    jump = cv2.imread("samples/jump.png")
    bus = cv2.imread("samples/bus.png")

    # convert the images to grayscale
    #storm = cv2.cvtColor(storm, cv2.COLOR_BGR2GRAY)
    #move = cv2.cvtColor(move, cv2.COLOR_BGR2GRAY)
    #jump = cv2.cvtColor(jump, cv2.COLOR_BGR2GRAY)
    #bus = cv2.cvtColor(bus, cv2.COLOR_BGR2GRAY)

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def get_no_from_name(name):
    if "/" in name:
        name = name.split("/")[1]
    else:
        name = name.split(".")[1]
    name = name.split("_")[1]
    name = name.split(".")[0]
    return name


if __name__ == "__main__":
    fd = sys.argv[1]

    read_sample_images()

    analyze_folder(fd)
