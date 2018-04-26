# pip3 install heatmappy
# python3 only!
# https://github.com/LumenResearch/heatmappy
import sys
from heatmappy import Heatmapper
from PIL import Image

class Fields:
    frameNr, x_pos, y_pos, omitFrame = range(0,4)

points = []

def ingest_file_content(file_path):
    with open(file_path, 'r') as file:
        for line in file.readlines()[1:]: # skip over header
            parts = line.split()
            if parts[Fields.omitFrame] == '1': continue
            points.append((int(parts[Fields.x_pos]), int(parts[Fields.y_pos])))

for file_path in sys.argv[1:]:
    ingest_file_content(file_path)
    print("processed " + file_path)

map_path = 'map.png'
map_img = Image.open(map_path)

heatmapper_cutout = Heatmapper(point_diameter=50,  # the size of each point to be drawn
    point_strength=0.005,  # the strength, between 0 and 1, of each point to be drawn
    opacity=0.8,  # the opacity of the heatmap layer
    colours='reveal',  # 'default' or 'reveal'
                        # OR a matplotlib LinearSegmentedColorMap object
                        # OR the path to a horizontal scale image
    grey_heatmapper='PIL'  # The object responsible for drawing the points
                           # Pillow used by default, 'PySide' option available if installed
)

heatmapper = Heatmapper(point_diameter=50,  # the size of each point to be drawn
    point_strength=0.02,  # the strength, between 0 and 1, of each point to be drawn
    opacity=0.8,  # the opacity of the heatmap layer
    colours='default',  # 'default' or 'reveal'
                        # OR a matplotlib LinearSegmentedColorMap object
                        # OR the path to a horizontal scale image
    grey_heatmapper='PIL'  # The object responsible for drawing the points
                           # Pillow used by default, 'PySide' option available if installed
)

heatmap = heatmapper.heatmap_on_img(points, map_img)
heatmap.save('heatmap.png')
print("written heatmap.png")

heatmap_cutout = heatmapper_cutout.heatmap_on_img(points, map_img)
heatmap_cutout.save('heatmap_cutout.png')
print("written heatmap_cutout.png")