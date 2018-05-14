import numpy as np
import cv2
import os
import time
# import Image
# from object_detection.obj_detection import detect_obj
from PIL import Image
from alexa import Alexa


class Edge():
    def __init__(self, id, url = 'http://cnx.ddns.net', port = '8000'):
        self.id = id
        self.previous_frame = None

    def imageDifferent(self, img1, img2, pixel_thresh=1, total_thresh=3.0):
        '''
        Assume input images size are the same
        '''
        diff = abs(img1-img2)
        threshold = diff[ np.where( diff >= pixel_thresh ) ]
        count = len(threshold)
        result = float(count)/float(np.prod(img1.shape))
        # print(result)
        return (result > total_thresh)

    # def 