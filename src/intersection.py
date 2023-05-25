import numpy as np

def compute_intersections(incisions, stitches):
    intersections = list()
    
    for incision in incisions:
        for stitch in stitches:
            if np.array_equal(incision, stitch[0]):
                intersections.append(incision)
            elif np.array_equal(incision, stitch[1]):
                intersections.append(incision)
                
    return np.unique(intersections, axis=0)

def compute_relative_intersections(intersections, first_incision):
    relative_intersections = list()
    
    for intersect in intersections:
        relative_intersections.append(np.linalg.norm(intersect - first_incision))

    return relative_intersections