from PIL import Image

def process():
    im = Image.open("/ndnSim/PythonScripts/fortnite/heatmap/heatmap_cutout_norm.png")
    pix = im.load()

    propability_vector = []

    for x in range(0, 1500):
        for y in range(0, 1500):
            mult = 1
            value = pix[x, y][0]
            if value > 200:
                mult = 8
            elif value > 150:
                mult = 7
            elif value > 100:
                mult = 6
            elif value > 50:
                mult = 3

            propability_vector += [(x, y)] * mult

    return propability_vector


def read_pois():
    im = Image.open("/ndnSim/PythonScripts/fortnite/heatmap/heatmap_erroded_dilated.png")
    pix = im.load()

    poi_vector = []

    for x in range(0, 1500):
        for y in range(0, 1500):
            if pix[x,y][0] > 200:
                poi_vector.append(((x-37)/142.7, (y-37)/142.7))

    return poi_vector