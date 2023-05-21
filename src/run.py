import sys
import matplotlib.pyplot as plt
import classification
import description
import preprocessing
import segmentation

from skimage.io import imread
from skan import draw

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

svc = classification.read_model()

for file in inputFiles:
    img = imread(file)

    if visualisation:
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.imshow(img, cmap='gray')

    img = preprocessing.convert_to_grayscale(img)
    img = segmentation.create_segmentation(img)
    segmentation.convert_to_binary(img)
    img = segmentation.remove_separate_points(img)
    branch_data = description.describe_objects(img)

    if visualisation:
        plt.subplot(2, 1, 2)
        draw.overlay_euclidean_skeleton_2d(img, branch_data, skeleton_color_source='branch-type')
        plt.imshow(img, cmap='gray')

    classification.classify(svc, branch_data)

