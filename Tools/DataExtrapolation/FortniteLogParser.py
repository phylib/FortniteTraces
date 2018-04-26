import sys
import glob
import time
import datetime

def find_log_files(location="."):
    if location[-1] != "/":
        location += "/"

    log_files = glob.glob(location + "*.log")

    traces = []
    for log_file in log_files:
        traces += extract_information(log_file)


    traces.sort()
    for log in traces:
        print(log)



def extract_information(log_file):
    with open(log_file) as f:
        file_content = f.readlines()[1:]
        f.close()

        logs = []

        for line in file_content:
            # Filter logs where Game State changes
            if "LogGameState" not in line:
                continue

            timestamp = line.split("]")[0][1:]

            t = datetime.datetime.strptime(timestamp, "%Y.%m.%d-%H.%M.%S:%f")
            t += datetime.timedelta(hours=1)

            current_game_state = line.split(" ")[-1].strip()

            logs.append((t.strftime("%Y-%m-%d %H:%M:%S.%f")[0:-3] + "\t" + current_game_state).strip())

        return logs


if __name__ == "__main__":
    folder = sys.argv[1]
    find_log_files(folder)