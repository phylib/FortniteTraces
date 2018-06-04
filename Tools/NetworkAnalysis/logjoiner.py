import os
import sys

SEPARATOR = "\t"

#
# main entry point of the application
#
if len(sys.argv) < 4:
    print('usage: python3 ' + sys.argv[0] + ' <input-file1> <input-file2> <output-file>\n')
    sys.exit()

first_file = {}
with open(sys.argv[1], "r") as input1:
    for line in input1.readlines():
        parts = line.split()
        first_file[parts[0] + " " + parts[1]] = parts[2:]

with open(sys.argv[3],"w") as output:
    with open(sys.argv[2],"r") as input2:
        for line in input2.readlines():
            parts = line.split()
            time_point = parts[0] + " " + parts[1]

            if time_point in first_file:
                output.write(line.rstrip() + SEPARATOR + SEPARATOR.join(first_file[time_point]) + "\n")
            else:
                output.write(line)