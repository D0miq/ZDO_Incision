import numpy as np
import xmltodict


def get_points(points):
    pts = points.split(";")
    return np.array([pt.split(",") for pt in pts], dtype=float)


def read_annotations():
    with open('../data/anotated_images/annotations.xml') as fd:
        doc = xmltodict.parse(fd.read())

    train_data = list()
    train_target = list()
    for image in doc["annotations"]["image"]:
        if "polyline" not in image:
            continue

        if type(image["polyline"]) is list:
            list_polylines = image["polyline"]
        else:
            list_polylines = [image["polyline"]]

        for pline in list_polylines:

            label = pline["@label"]
            if label == "Incision":
                target = -1  # Incision = -1
            else:
                target = 1  # Stitch = 1

            pts = get_points(pline["@points"])
            pts_list = (list(zip(pts[:, 0], pts[:, 1])))

            for start, end in zip(pts_list, pts_list[1:]):
                vector = np.array(end) - np.array(start)
                distance = np.linalg.norm(vector)
                train_data.append([vector[0] / distance, vector[1] / distance])
                train_target.append(target)

    return [train_data, train_target]
