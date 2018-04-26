import os
import sys
import datetime

CLIENT_MSG_CNT = "#client-msg"
SERVER_MSG_CNT = "#server-msg"
CLIENT_BYTES_SUM = "client-msg-bytes-sum"
SERVER_BYTES_SUM = "server-msg-bytes-sum"


#
# main entry point of the application
#
def execute(input_file, output_file):

    intervals = {}
    with open(input_file, "r") as input_file:
        for line in input_file.readlines()[1:]:
            # 2018-02-08 17:05:29.384909	out	udp:data	25	67
            # 2018-02-08 17:05:29.445468	in	udp:data	25	67
            parts = line.split()

            # "2018-02-08 17:05:29.384909" => "2018-02-08 17:05:29"
            time_index = parts[0] + " " + parts[1].split('.')[0]
            if not time_index in intervals:
                intervals[time_index] = {CLIENT_MSG_CNT: 0, SERVER_MSG_CNT: 0, CLIENT_BYTES_SUM: 0, SERVER_BYTES_SUM: 0}

            # categorize packet (client-sent / server-sent packet)
            if parts[2] == "out":
                intervals[time_index][CLIENT_MSG_CNT] += 1  # register client-/server-packet
                intervals[time_index][CLIENT_BYTES_SUM] += int(parts[4])  # sum up client-/server-sent bytes
            elif parts[2] == "in":
                intervals[time_index][SERVER_MSG_CNT] += 1
                intervals[time_index][SERVER_BYTES_SUM] += int(parts[4])
            else:
                raise ValueError("invalid direction, must be either 'in' or 'out")

    with open(output_file, "w") as output_file:
        output_file.write(
            "time-point\t" + CLIENT_MSG_CNT + "\t" + SERVER_MSG_CNT + "\tclient-bytes\tserver-bytes\tavg-client-bytes\tavg-server-bytes\n")
        for time_point in sorted(list(intervals.keys())):
            entry = intervals[time_point]
            avg_client_bytes = "0" if entry[CLIENT_MSG_CNT] == 0 else format(
                entry[CLIENT_BYTES_SUM] / entry[CLIENT_MSG_CNT], '.2f')
            avg_server_bytes = "0" if entry[SERVER_MSG_CNT] == 0 else format(
                entry[SERVER_BYTES_SUM] / entry[SERVER_MSG_CNT], '.2f')
            output_file.write(time_point + "\t" + str(entry[CLIENT_MSG_CNT]) + "\t" + str(entry[SERVER_MSG_CNT]) +
                              "\t" + str(entry[CLIENT_BYTES_SUM]) + "\t" + str(
                entry[SERVER_BYTES_SUM]) + "\t" + avg_client_bytes + "\t" + avg_server_bytes + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('usage: python3 ' + sys.argv[0] + ' <input-file> <output-filename>\n')
        sys.exit()
    execute(sys.argv[1], sys.argv[2])
