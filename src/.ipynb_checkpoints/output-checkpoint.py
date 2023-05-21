import json

def write_to_output(output_file, img_name, polyline, crossing_positions, crossing_angles):
    data = [
        { "filename": img_name,
          "incision_polyline": polyline, # [[ 109.47, 19.32],[111.88,42.19]]
          "crossing_positions": crossing_positions, # [13.8, 18.1, 19.0]
          "crossing_angles": crossing_angles, # [87.1, 92.3, 75.0]
        }, 
      ]


    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)