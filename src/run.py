import sys
import matplotlib.pyplot as plt

from skan import draw
from skimage.io import imread

import angle
import annotations
import classification
import description
import intersection
import output
import preprocessing
import segmentation
import input_parser

if not sys.argv[1].endswith(".json"):
    print("Output json is not specified")
    sys.exit()

output_file = sys.argv[1]

if sys.argv[2] == "-v":
    visualisation = True
    input_paths = sys.argv[3:]
else:
    visualisation = False
    input_paths = sys.argv[2:]

if len(input_paths) == 0:
    print("No input files are specified")
    sys.exit()

input_files = input_parser.get_input_files(input_paths)

svc = classification.create_svm()
[train_data, train_target] = annotations.read_annotations()
svc.fit(train_data, train_target)

global_relative_intersections = list()
global_incisions = list()
global_angles = list()

for file in input_files:
    print(f"File:{file}")
    img = imread(file)

    if visualisation:
        plt.figure()
        plt.imshow(img)

    img = preprocessing.convert_to_grayscale(img)

    if visualisation:
        plt.figure()
        plt.imshow(img, cmap='gray')

    # Segmentace
    img = segmentation.create_segmentation(img)
    segmentation.convert_to_binary(img)
    img = segmentation.remove_separate_points(img)

    # Skeletonization
    try:
        branch_data = description.create_branches(img)
    except:
        print("Unable to retrieve data from a skelet\n")
        global_relative_intersections.append(list())
        global_incisions.append(list())
        global_angles.append(list())
        continue

    if visualisation:
        draw.overlay_euclidean_skeleton_2d(img, branch_data)

    # Klasifikace
    features = description.get_feature_vector(branch_data)
    branch_types = classification.classify(svc, features)
    print(f"Prediction:{branch_types}")

    # Výpočet incisions a stitches
    (incisions, stitches) = description.get_incisions_and_stitches(branch_types, branch_data)
    print(f"Incisions:{incisions}")
    print(f"Stitches:{stitches}")

    global_incisions.append(incisions)

    # Výpočet průsečíků
    intersections = intersection.compute_intersections(incisions, stitches)
    print(f"Intersections:{intersections}")

    relative_intersections = list()
    if len(incisions) > 0:
        relative_intersections = intersection.compute_relative_intersections(intersections, incisions[0])

    global_relative_intersections.append(relative_intersections)

    # Výpočet úhlů
    angles = angle.compute_angles(incisions, stitches, intersections)
    print(f"Angles:{angles}\n")

    global_angles.append(angles)

    if visualisation:
        plt.show()

output.write_to_output(output_file, input_files, global_incisions, global_relative_intersections, global_angles)
