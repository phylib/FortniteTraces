import os
import sys
import datetime
from datetime import datetime
import matplotlib.pyplot as plt


#
# main entry point of the application
#
if len(sys.argv) < 2:
    print('usage: python3 ' + sys.argv[0] + ' <input-file>\n')
    sys.exit()
time_points = []
client_msg_cnt = []
server_msg_cnt = []
client_bytes = []
server_bytes = []
client_bytes_avg = []
server_bytes_avg = []

with open(sys.argv[1], "r") as input_file:
    for line in input_file.readlines()[1:]:
        parts = line.split()  # 2018-02-08 18:40:33	18	13	2563	299	142.39	23.00
        time_points.append(datetime.strptime(parts[0] + " " + parts[1], '%Y-%m-%d %H:%M:%S'))
        client_msg_cnt.append(int(parts[2]))
        server_msg_cnt.append(int(parts[3]))
        client_bytes.append(int(parts[4]))
        server_bytes.append(int(parts[5]))
        client_bytes_avg.append(float(parts[6]))
        server_bytes_avg.append(float(parts[7]))


plt.subplot(3, 1, 1)
plt.plot(time_points, client_msg_cnt, color="r", label='#client-msgs')
plt.plot(time_points, server_msg_cnt, color="g", label='#server-msgs')
plt.title('Messages/s')
plt.ylabel('#')

plt.subplot(3, 1, 2)
plt.plot(time_points, client_bytes, color="r", label='#client-bytes-avg')
plt.plot(time_points, server_bytes, color="g", label='#server-bytes-avg')
plt.title('msg Bytes/s')
plt.ylabel("Byte/s")


plt.subplot(3, 1, 3)
plt.plot(time_points, client_bytes_avg, color="r", label='#client-bytes-avg')
plt.plot(time_points, server_bytes_avg, color="g", label='#server-bytes-avg')
plt.title('average msg Bytes/s')
plt.ylabel("Byte/s")

#plt.tight_layout()
plt.show()