from skimage.color import rgb2gray
from skimage.exposure import rescale_intensity


def convert_to_grayscale(img):
    grayscale = rgb2gray(img) * 255
    return rescale_intensity(grayscale, out_range=(0, 255))
