import cv2
import numpy as np
import requests
from StringIO import StringIO

Class Video_handler():
    def __init__(url, port):
        self.url = url
        self.port = port
        self.address = url+':'+port

    def read_video(file_path):
        cap = cv2.VideoCapture(file_path)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

        return buf

    def upload(frame):
        img_content = frame.tostring()
        requests.post('{}:{}/{}?img={}'.format(self.url, self.port, self.up_func, img_content)

