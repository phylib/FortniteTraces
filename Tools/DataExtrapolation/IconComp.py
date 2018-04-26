# import the necessary packages
#from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


# load the images -- the original, the original + contrast,
# and the original + photoshop
storm = cv2.imread("storm.png")
move = cv2.imread("move.png")
jump = cv2.imread("jump.png")
bus = cv2.imread("bus.png")
test = cv2.imread("storm_0117.png_prep.png")

# convert the images to grayscale
storm = cv2.cvtColor(storm, cv2.COLOR_BGR2GRAY)
move = cv2.cvtColor(move, cv2.COLOR_BGR2GRAY)
jump = cv2.cvtColor(jump, cv2.COLOR_BGR2GRAY)
bus = cv2.cvtColor(bus, cv2.COLOR_BGR2GRAY)
test = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

print("Storm: " + str(mse(storm, test)))
print("Move: " + str(mse(move, test)))
print("Jump: " + str(mse(jump, test)))
print("Bus: " + str(mse(bus, test)))

