# sudo apt install tshark
# pip3 install pyshark
import os
import sys
import pyshark
import datetime
from multiprocessing import Pool

OUTPUT_DIR=""
CLIENT_IP=""
FILTER_EXPR=""


def parse_date(date_string):
    # 'Jan  1, 1970 01:00:01.006672000 CET'   # .%f down to microsecond precition (ns not supported!) + discard timezone
    return datetime.datetime.strptime(date_string.rsplit(' ', 1)[0], '%b %d, %Y %H:%M:%S.%f000')

def process_PCAP_file(pcap_filename):
    filename = pcap_filename.split("/")[-1]
    target_filename = os.path.join(OUTPUT_DIR, filename.split(".")[0] + ".csv")

    log_lines = []
    f = pyshark.FileCapture(pcap_filename, display_filter=FILTER_EXPR)

    # store relevant information about received Packets
    for packet in f:
        if packet.ip.src == CLIENT_IP:
            direction = "out"
        elif packet.ip.dst == CLIENT_IP:
            direction = "in"
        else: continue

        try:
            data_size = packet[packet.highest_layer].len
        except:
            data_size = 0

        time = parse_date(packet.frame_info.time.__str__())
        total_size = packet.length
        log_lines.append(str(time) + "\t" + direction + "\t" + ":".join(packet.frame_info.protocols.split(":")[-2:]) + "\t" + str(data_size) + "\t" +  str(total_size))
    f.close()

    # write log_lines to file
    with open(target_filename, "w") as log_file:
        log_file.write("time\tin/out\tprotocol\tpayload-size\ttotal-size\n")
        log_file.write("\n".join(log_lines))

    print(target_filename + ": created")
    del log_lines


#
# main entry point of the application
#
if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print('usage: python3 ' + sys.argv[0] + ' <output-dir> <client-ip-address> <wireshark-display-filter-expr> <pcap-file#1>  ...\n')
        print('python3 pcapprocessor.py ./ 192.168.1.165 "ip" ../traces/2018-02-08_FNBR_g1.pcap')
        print('python3 pcapprocessor.py ./ 192.168.1.165 "udp and ip.addr == 192.168.1.165" ../traces/2018-02-08_FNBR_g1.pcap')
        print('python3 pcapprocessor.py ./ 192.168.1.165 "udp and data and ip.addr == 192.168.1.165 and not ip.addr == 230.0.0.1" ../traces/2018-02-08_FNBR_g1.pcap')
        sys.exit()

    OUTPUT_DIR = sys.argv[1]
    CLIENT_IP = sys.argv[2]
    FILTER_EXPR = sys.argv[3]

    p = Pool(2)
    p.map(process_PCAP_file, sys.argv[4:])
    p.close()
    p.join()
