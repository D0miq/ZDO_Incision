import numpy as np

from skan import Skeleton, summarize
from skimage import morphology


def create_branches(img):
    skelet = morphology.skeletonize(img)
    return summarize(Skeleton(skelet))


def get_feature_vector(branch_data):
    distances = branch_data['euclidean-distance']
    coord_img_src_x = branch_data['image-coord-src-1']
    coord_img_src_y = branch_data['image-coord-src-0']
    coord_img_dst_x = branch_data['image-coord-dst-1']
    coord_img_dst_y = branch_data['image-coord-dst-0']

    result = np.array([list(a) for a in zip((coord_img_dst_x - coord_img_src_x) / distances,
                                            (coord_img_dst_y - coord_img_src_y) / distances)])
    result[np.isnan(result)] = 0
    return result


def get_incisions_and_stitches(branch_types, branch_data):
    incisions = list()
    stitches = list()

    for i in range(0, len(branch_types)):
        start = np.array([branch_data['image-coord-src-1'][i], branch_data['image-coord-src-0'][i]])
        end = np.array([branch_data['image-coord-dst-1'][i], branch_data['image-coord-dst-0'][i]])

        if start[0] > end[0]:
            temp = start
            start = end
            end = temp

        if branch_types[i] == -1:
            if len(incisions) == 0:
                incisions.append(start)
                incisions.append(end)
            else:
                j = len(incisions) - 1
                while j >= 0 and incisions[j][0] > start[0]:
                    j -= 1

                if j == -1:
                    incisions.insert(0, start)
                elif j == len(incisions) - 1:
                    if not np.array_equal(incisions[j], start):
                        incisions.append(start)
                    incisions.append(end)
                else:
                    if not np.array_equal(incisions[j], start):
                        incisions.insert(j + 1, start)
        else:
            stitches.append(tuple([start, end]))

    return tuple([incisions, stitches])
