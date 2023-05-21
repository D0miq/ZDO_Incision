from skan import Skeleton, summarize
from skimage import morphology

def create_branches(img):
    skelet = morphology.skeletonize(img)
    return summarize(Skeleton(skelet))

# Z branch_data získá euklidovskou vzdálenost a image coord ve tvaru [distance, coord-src-0_src, coord-src-1_src, coord-dst-0_dst, coord-dst-1_dst] pro každou část skeletu
def get_feature_vector(branch_data):
    distances = branch_data['euclidean-distance']
    coord_img_src0 = branch_data['image-coord-src-0']
    coord_img_src1 = branch_data['image-coord-src-1']
    coord_img_dst0 = branch_data['image-coord-dst-0']
    coord_img_dst1 = branch_data['image-coord-dst-1']
    
    
    # klíče z dictinary: euclidean-distance, image-coord-src-0, image-coord-src-1,
    # image-coord-dst-0, image-coord-dst-1
    
    #selected_keys = ["euclidean-distance", "image-coord-src-0", "image-coord-src-1",
    # "image-coord-dst-0", "image-coord-dst-1"]
    
    #res_dict = {key: branch_data.head()[key] for key in branch_data.head().keys() & selected_keys}
    
    ##   [dis_skelet_2, start_x_skelet_2, start_y_skelet_2... ], 
    ## Z branch_data získá euklidovskou vzdálenost a image coord ve tvaru [distance, coord-src-0_src, coord-src-1_src, coord-dst-0_dst, coord-dst-1_dst] pro každou část skeletu
    
    # [ [dis_skelet_1, start_x_skelet_1, start_y_skelet_1... ],
    #   [dis_skelet_2, start_x_skelet_2, start_y_skelet_2... ],
    # ]
    
    return [list(a) for a in zip(distances, coord_img_dst0 - coord_img_src0, coord_img_dst1 - coord_img_src1)]
    #return list(branch_data.head().values())
    #return [distances,coord_img_src0,coord_img_src1, coord_img_dst0,coord_img_dst1]
