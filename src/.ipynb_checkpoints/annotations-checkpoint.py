import xmltodict
import numpy as np
import line_intersection

def get_points(points,):
    pts = points.split(";")
    return np.array([pt.split(",") for pt in pts], dtype=float)

def read_annotations():
    with open('../data/anotated_images/annotations.xml') as fd:
        doc = xmltodict.parse(fd.read())

    train_data = list()
    train_target = list()
    for image in doc["annotations"]["image"]:
        if not "polyline" in image:
            continue

        list_polylines = []
        if type(image["polyline"]) is list:
            list_polylines = image["polyline"]
        else:    
            list_polylines = [image["polyline"]]

        for pline in list_polylines:
            
            label = pline["@label"]
            if label == "Incision":
                target = -1 # Incision = -1
            else:
                target = 1 # Stitch = 1

            pts = get_points(pline["@points"])
            pts_list = (list(zip(pts[:,0],pts[:,1])))

            for start, end in zip(pts_list, pts_list[1:]):
                # Vypočítat vzdálenost mezi krajními body jedné části pline
                vector = np.array(end) - np.array(start)
                distance = np.linalg.norm(vector)
                
                # Vložit data do train_data a train_target
                # train_data[i] = [distance, coord-src-0, coord-src-1, coord-dst-0, coord-dst-1]
                # train_target[i] = 1 nebo -1
                train_data.append([distance, vector[0], vector[1]])
                train_target.append(target)

            # Zkontrolovat průsečíky pline se všemi ostatními polylinami jiného typu.
            # Když se průsečík najde, tak pline rozdělit na dvě části
            #for pline2 in image["polyline"]:
            #    if not label == pline2["@label"]:
            #        pts2 = get_points(pline2)
            #        x, y, valid, r, s = line_intersection.intersectLines(pts[0,:], pts[1,:], pts2[0,:], pts2[1,:])
            #        if valid == 1:

    return [train_data, train_target]

