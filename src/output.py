import json
import numpy as np
import numpy
#from json_stream import streamable_list


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def write_to_output(output_file, img_name, polyline, crossing_positions, crossing_angles):
    data = list()

    for i in range(0, len(img_name)):
        element = { 
            "filename": img_name[i],
            "incision_polyline": polyline[i],
            "crossing_positions": crossing_positions[i],
            "crossing_angles": crossing_angles[i],
        }
        data.append(element)
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, cls=NumpyEncoder)

#import sys
#import json
#wrap existing iterable
#data = streamable_list(range(10))
# consume iterable with standard json.dump()
#json.dump(data, sys.stdout)