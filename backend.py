import hug

import cv2
import json
import numpy as np

@hug.post('/img_upload')
def take_img( body):
    # cli_id = int(cli_id)
    img = body['img']
    np_img = np.frombuffer(img, dtype=np.int8)
    info = json.loads(body['info'].decode('utf8'))
    shape = info['size']
    print(info['id'])
    np_img = np_img.reshape(shape)
    print(np_img.shape)
