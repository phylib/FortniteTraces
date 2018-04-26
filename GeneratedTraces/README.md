# Description of created files

## player_XY_movement.csv

This file contains the movement trace of the player. It ends when the player dies or the game ends.

**Columns**:

* time: Time since start of the game in seconds
* x-coord: x-position of the player (range: 0 - 10)
* y-coord: y-position of the player (range: 0 - 10)

## player_XY_packet_log.csv

This file contains information about every single extrapolated packet on a client.

**Columns:**

* time: Unix Timestamp
* in/out: Is the packet incoming (from server to client) or outgoing (from client to server)
* protocol: TCP or UDP packet
* payload-size: Size of the transported payload
* total-size: Total size of resulting packet, including packet headers

## player_XY_game_info.csv

Contains general information about the game and the current player.

**Columns:**

* time: Unix Timestamp
* time in seconds since start of the game
* time in seconds since start of the game
* Current number of active players in the game
* Current phase in the game
* State of the player (alive/dead)

## player_XY_averages_packet_log.csv

Averaged network packet information in one-second intervals.

**Columns:**

* time: Unix timestamp
* #client-msg: Number of client packets per second
* #server-msg: Number of server packets per second
* client-bytes: Overall payload sent by the client in the corresponding second
* server-bytes: Overall payload sent by the server in the corresponding second
* avg-client-bytes: avg payload size of client packets in the corresponding second
* avg-server-bytes: avg payload size of server packets in the corresponding second

## player_XY_joined.csv

Combines the content from `player_XY_game_info.csv` and `player_XY_averages_packet_log.csv`.
