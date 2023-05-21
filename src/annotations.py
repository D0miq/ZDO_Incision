import xmltodict
import numpy as np


def read_annotations():
    with open('data/annotations.xml') as fd:
        doc = xmltodict.parse(fd.read())

    for image in doc["annotations"]["image"]:
        for pline in image["polyline"]:
            # extract coodrinates
            pts = np.array([pt.split(",") for pt in pline["@points"].split(";")], dtype=float)
