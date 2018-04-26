This folder contains the tools to extrapolate movement and network traces, as well as tools for visualizing those generated traces.

When new traces should be created, please focus on the `TrafficGenerator.py` script. This script first generates movement traces using the `FortniteWorldGeneration.py` script, writes the resulting movement traces into the output folder and then creates traffic traces, based on the player movements.

The script can be started using the following command:

    python TrafficGenerator.py -o output/ -g 0 -c true -v true

The `-o` option defines the output folder, the `-g` defines an ID for the game to create. It is used to seed random generators. Whenever the same game ID is selected, the script results in the same output. `-c` defines wheter graphs should be created or not. More information about possible parameters can be found with `python TrafficGenerator.py -h`.

In order to visualize the traffic load of the Fortnite Server, the script `serverloadsum.py` can be used. In order to generate a chart, as it can be found in the corresponding paper, the following command can be used:

    python serverloadsum.py -i output/ -s 5 -o serverload.pdf

For detailed information about the usage, please use `python serverloadsum.py -h`.
