import numpy as np

def compute_angle(vectorA, vectorB):
    unit_vectorA = vectorA / np.linalg.norm(vectorA)
    unit_vectorB = vectorB / np.linalg.norm(vectorB)
    return np.rad2deg(np.arccos(np.clip(np.dot(unit_vectorA, unit_vectorB), -1.0, 1.0)))

def compute_angles(incisions, stitches, intersections):
    angles = list()
    stitch_vector = np.zeros(2)
    incision_vector = np.zeros(2)

    for intersection in intersections:
        for stitch in stitches:
            if np.array_equal(stitch[0], intersection):
                if stitch[0][1] - stitch[1][1] > 0:
                    stitch_vector = stitch[1] - stitch[0]
                else:
                    stitch_vector = stitch[0] - stitch[1]
                break;
            elif np.array_equal(stitch[1], intersection):
                if stitch[1][1] - stitch[0][1] > 0:
                    stitch_vector = stitch[0] - stitch[1]
                else:
                    stitch_vector = stitch[1] - stitch[0]
                break;


        for i in range(0, len(incisions)):
            if np.array_equal(incisions[i], intersection):
                if i == len(incisions) - 1:
                    incision_vector = incisions[i] - incisions[i - 1]
                else:
                    incision_vector = incisions[i + 1] - incisions[i]
                break;

        angles.append(compute_angle(stitch_vector, incision_vector))

    return angles