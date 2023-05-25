import sys
import matplotlib.pyplot as plt

from skan import draw
from skimage.io import imread

import annotations
import classification
import description
import output
import preprocessing
import segmentation
import angle
import intersection

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

if len(inputFiles) == 0:
    print("No input files are specified")
    sys.exit()

svc = classification.create_svm()
[train_data, train_target] = annotations.read_annotations()
svc.fit(train_data, train_target)

global_relative_intersections = list()
global_incisions = list()
global_angles = list()

for file in inputFiles:
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
        sys.exit()
    
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
    
    global_relative_intersections.append(intersection.compute_relative_intersections(intersections, incisions[0]))
    
    # Výpočet úhlů
    angles = angle.compute_angles(incisions, stitches, intersections);
    print(f"Angles:{angles}\n")
    
    global_angles.append(angles)
    
output.write_to_output(outputFile, inputFiles, global_incisions, global_relative_intersections, global_angles)