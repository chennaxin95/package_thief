import cv2
import json
import numpy as np
import requests
from io import StringIO
import datetime
import time

class Alexa():
    def __init__(self, id, url='http://cnx.ddns.net', port='8000', up_func='img_upload',
                 online_func='go_online'):
        self.url = url
        self.port = port
        self.address = url+':'+port
        self.up_func = up_func
        self.online_func = online_func
        self.id = id
        self.previous_frame = None
        self.buffer = None

    def go_online(self):
        a = requests.post('{}:{}/{}?id={}'.format(self.url, self.port, self.online_func, self.id))
        print a

    def read_video(self, file_path):
        cap = cv2.VideoCapture(file_path)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
        success = True
        success, frame = cap.read()
        count = 0
        while success:
            buf[count] = frame
            success, frame = cap.read()
            count += 1
            print(frame)
        buf = np.rollaxis(buf, 3, 1)
        self.buffer = buf
        return buf.shape

    def upload(self, frame):
        ts = time.time()
        stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        info = {'id' : self.id,
                'size' : frame.shape,
                'time' : stamp}
        a = requests.post('{}:{}/{}'.format(self.url, self.port, self.up_func), 
            files={'img':frame.tobytes(),
                    'info':json.dumps(info)})
        print(a)

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
    
    def stream(self, fps):
        # upload(frame) based on fps if frame is different than before
        i = 0
        while not (self.buffer is None):
            for frame in self.buffer: 
                if self.previous_frame is None:
                    self.previous_frame = frame
                else:
                    if self.imageDifferent(self.previous_frame, frame):
                        print(self.imageDifferent(self.previous_frame,frame))
                        self.upload(frame)
                        self.previous_frame = frame
                time.sleep(1.0/float(fps))
                # print(i)
                i+=1
            self.buffer = None
            i = 0