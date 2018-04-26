import os
import sys

SEPARATOR = "\t"


def execute(input_file_1, input_file_2, output_file):
    first_file = {}
    with open(input_file_1, "r") as input1:
        for line in input1.readlines():
            parts = line.split()
            first_file[parts[0] + " " + parts[1]] = parts[2:]

    with open(output_file, "w") as output:
        with open(input_file_2, "r") as input2:
            for line in input2.readlines():
                parts = line.split()
                time_point = parts[0] + " " + parts[1]

                if time_point in first_file:
                    output.write(line.rstrip() + SEPARATOR + SEPARATOR.join(first_file[time_point]) + "\n")
                else:
                    output.write(line)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('usage: python3 ' + sys.argv[0] + ' <input-file1> <input-file2> <output-file>\n')
        sys.exit()
    execute(sys.argv[1], sys.argv[2], sys.argv[3])
