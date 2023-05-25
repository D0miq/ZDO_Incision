import numpy as np

from skan import Skeleton, summarize
from skimage import morphology


def create_branches(img):
    skelet = morphology.skeletonize(img)
    return summarize(Skeleton(skelet))


# Z branch_data získá euklidovskou vzdálenost a image coord ve tvaru [distance, coord-src-0_src, coord-src-1_src, coord-dst-0_dst, coord-dst-1_dst] pro každou část skeletu
def get_feature_vector(branch_data):
    distances = branch_data['euclidean-distance']
    coord_img_srcX = branch_data['image-coord-src-1']
    coord_img_srcY = branch_data['image-coord-src-0']
    coord_img_dstX = branch_data['image-coord-dst-1']
    coord_img_dstY = branch_data['image-coord-dst-0']
    # ]
    result = np.array([list(a) for a in zip((coord_img_dstX - coord_img_srcX) / distances, (coord_img_dstY - coord_img_srcY) / distances)])
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