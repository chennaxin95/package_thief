import cv2
import json
import numpy as np
import requests
from io import StringIO

class Video_handler():
    def __init__(self, url, port, up_func, id):
        self.url = url
        self.port = port
        self.address = url+':'+port
        self.up_func = up_func
        self.id = id

    def read_video(self, file_path):
        cap = cv2.VideoCapture(file_path)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

        return buf

    def upload(self, frame):
        # img_content = frame.tostring()
        info = {'id' : self.id,
                'size' : frame.shape}
        a = requests.post('{}:{}/{}'.format(self.url, self.port, self.up_func), 
            files={'img':frame.tobytes(),
                    'info':json.dumps(info)})
        print(a)
