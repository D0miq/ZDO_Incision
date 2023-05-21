import sys
import numpy as np
import matplotlib.pyplot as plt

from skimage import morphology
from skimage.segmentation import watershed
from skimage.color import rgb2gray
from skimage.exposure import rescale_intensity
from skimage.io import imread
from skimage.filters import sobel
from skan import Skeleton, summarize, draw
from sklearn import svm

def preprocess(img):
    grayscale = rgb2gray(img) * 255
    return rescale_intensity(grayscale, out_range=(0, 255))


def create_segmentation(img):
    # region based segmentation
    elevation_map = sobel(img)

    markers = np.zeros_like(img)
    markers[img < 100] = 1
    markers[img > 150] = 2

    return watershed(elevation_map, markers)


def convert_to_binary(img):
    # convert image to 0 and 1
    img[img < 1.5] = 1
    img[img > 1.5] = 0


def remove_separate_points(img):
    # morphology
    kernel = morphology.square(4)
    morph = morphology.binary_erosion(img, kernel)
    kernel = morphology.square(6)
    return morphology.binary_dilation(morph, kernel)


def describe_objects(img):
    skelet = morphology.skeletonize(img)
    return summarize(Skeleton(skelet))


def classify(testData):
    svc = svm.SVC()
    svc.fit(train_data, train_target)
    pred = svc.predict(testData)


if not sys.argv[1].endswith(".json"):
    print("Output json is not specified")
    sys.exit()

outputFile = sys.argv[1]

if sys.argv[2] == "-v":
    visualisation = True
    inputFiles = sys.argv[3:]
else:
    visualisation = False
    inputFiles = sys.argv[2:]

for file in inputFiles:
    img = imread(file)

    if visualisation:
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.imshow(img, cmap='gray')

    preprocess(img)
    img = create_segmentation(img)
    convert_to_binary(img)
    img = remove_separate_points(img)
    branch_data = describe_objects(img)

    if visualisation:
        plt.subplot(2, 1, 2)
        draw.overlay_euclidean_skeleton_2d(img, branch_data, skeleton_color_source='branch-type')
        plt.imshow(img, cmap='gray')

    classify(branch_data)

