import hug

import cv2
import numpy as np

@hug.post('/uploadIMG')
def take_img(cli_id, img):
    cli_id = int(cli_id)
    np_img = np.fromstring(img)
    _, w, h = np_img.shape
    print("got image size of {} x {}".format(w, h)) 
