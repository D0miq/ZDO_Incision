from skan import Skeleton, summarize
from skimage import morphology


def describe_objects(img):
    skelet = morphology.skeletonize(img)
    return summarize(Skeleton(skelet))
