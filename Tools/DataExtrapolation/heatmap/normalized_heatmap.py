import glob
import sys
import numpy
import time
import itertools
from heatmappy import Heatmapper
from PIL import Image

class Fields:
    frameNr, x_pos, y_pos, omitFrame = range(0,4)

heatmap = numpy.zeros((1500, 1500))
points = []

def ingest_file_content(file_path):
    with open(file_path, 'r') as file:
        for line in file.readlines()[1:]: # skip over header
            parts = line.split()
            if parts[Fields.omitFrame] == '1': continue
            heatmap[int(parts[Fields.x_pos])][int(parts[Fields.y_pos])] += 1


folder = sys.argv[1]
files = glob.glob(folder + "*.txt")

for file_path in files:
    start = time.time()
    ingest_file_content(file_path)
    end = time.time()
    print("processed " + file_path + " in " + str(end - start) + 's')

#numpy.savetxt("heatmap.csv", heatmap, delimiter=",")

# normalize count before handing it over to heatmappy
heatmap /= (heatmap.max()/100)

for j in range(len(heatmap)):
     for i in range(len(heatmap[0])):
        if heatmap[i][j] == 0: continue
        points += list(itertools.repeat((i,j), int(round(heatmap[i][j]))))

map_path = 'white.png'
map_img = Image.open(map_path)

heatmapper_cutout = Heatmapper(point_diameter=50,  # the size of each point to be drawn
    point_strength=0.005,  # the strength, between 0 and 1, of each point to be drawn
    opacity=1,  # the opacity of the heatmap layer
    colours='reveal',  # 'default' or 'reveal'
                        # OR a matplotlib LinearSegmentedColorMap object
                        # OR the path to a horizontal scale image
    grey_heatmapper='PIL'  # The object responsible for drawing the points
                           # Pillow used by default, 'PySide' option available if installed
)

heatmapper = Heatmapper(point_diameter=50,  # the size of each point to be drawn
    point_strength=0.02,  # the strength, between 0 and 1, of each point to be drawn
    opacity=1,  # the opacity of the heatmap layer
    colours='default',  # 'default' or 'reveal'
                        # OR a matplotlib LinearSegmentedColorMap object
                        # OR the path to a horizontal scale image
    grey_heatmapper='PIL'  # The object responsible for drawing the points
                           # Pillow used by default, 'PySide' option available if installed
)

heatmap = heatmapper.heatmap_on_img(points, map_img)
heatmap.save('heatmap_norm.png')

heatmap_cutout = heatmapper_cutout.heatmap_on_img(points, map_img)
heatmap_cutout.save('heatmap_cutout_norm.png')