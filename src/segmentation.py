import numpy as np

from skimage import morphology
from skimage.segmentation import watershed
from skimage.filters import sobel


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
