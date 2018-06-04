# Analyzing a Fortnite PCAP Trace

## General requirements

* wireshark
* tcpdump for pcap-file creation

## Requirements for pcap-processor.py
* Python 3
* sudo apt install tshark
* pip3 install pyshark

## Sample usage:

In the following, we explain how to analyze the provided sample PCAP File `2018-02-08_FNBR_g4.pcap`.

1) Use wireshark to gain an overview of the relevant traffic streams:

	$ wireshark traces/2018-02-08_FNBR_g4.pcap

Statistics/Conversations/UDP/ -> sort by desc. packet-number
find addresses of client/server (we mainly focus on UDP-traffic between client and server)
in our case 192.168.1.165 ("Address A" / our game-client) and 18.196.71.111 ("Address B" / the game-server)

we now can create a wireshark filter expression:

	udp and data and ip.addr==192.168.1.165 and ip.addr==18.196.71.111
	// "udp and data"   ... we concentrate on UDP traffic and wish to omit DNS-messages
    // "ip.addr==192.168.1.165 and ip.addr==18.196.71.111" ... we focus on the conversation between client and server

the filter-expression can be fine-tuned/tested using wireshark and is then used by `pcapprocessor.py` to extract the packet-information from the pcap-file.

    $ python3 pcapprocessor.py ./ 192.168.1.165 "udp and data and ip.addr==192.168.1.165 and ip.addr==18.196.71.111" ./traces/2018-02-08_FNBR_g4.pcap

More examples can be found in `perform_pcap_processing.sh`. pcapprocessor uses the python3 module `pyshark` to allow for the same freedom of expression (regarding the filter) as wireshark (uses tshark under the hood, -> a bit slow).

`pcapprocessor` creates one entry per (UDP-)-Packet. The result can be seen in e.g. `2018-02-08_FNBR_g4.csv`:

	time						in/out	protocol	payload-size	total-size
	2018-02-08 17:25:12.746374	out		udp:data	25				67
	2018-02-08 17:25:12.814373	in		udp:data	25				67
	2018-02-08 17:25:12.826409	out		udp:data	25				67
	2018-02-08 17:25:12.865460	in		udp:data	25				67
	2018-02-08 17:25:12.876894	out		udp:data	84				126

	// Perspective of the client -> in ... received by the client, out ... sent by the client  (from/to the server)


Now, based on this file, we can create a packet statistics (in one second-intervals) by using `trafficstat.py`:

	$ python3 trafficstat.py 2018-02-08_FNBR_g4.csv 2018-02-08_FNBR_g4_stat.csv

This results in `2018-02-08_FNBR_g4_stat.csv`:

    time-point	#client-msg	#server-msg	client-bytes	server-bytes	avg-client-bytes	avg-server-bytes
    2018-02-08 17:25:12	3	2	134	50	44.67	25.00
    2018-02-08 17:25:13	10	10	2374	239	237.40	23.90
    2018-02-08 17:25:14	17	44	961	12572	56.53	285.73
    2018-02-08 17:25:15	19	19	643	8275	33.84	435.53
    2018-02-08 17:25:16	21	20	1061	9764	50.52	488.20


`trafficplot.py` can be used to plot the contents of a traffic-statistics-file:

	$ python3 trafficplot.py 2018-02-08_FNBR_g4_stat.csv


`logjoiner.py` can be used to unite two logfiles, e.g. the extracted game-state log and the previously created traffic-statistics log. It works by joining the files based on the time-index (second, e.g. `2018-02-08 17:25:12`).

	$ logjoiner.py  gamestate_example.log 2018-02-08_FNBR_g4_stat.csv joined_logs.csv
