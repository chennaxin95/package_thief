import argparse
import cv2
import json
import redis
import numpy as np
from uuid import uuid4
from pprint import pprint
from twilio.rest import Client
from object_detection.obj_detection import Detector

from .celery import app

# SETTING UP CONSTANTS
account_sid = 'AC59f219f50e0c807bbef4a098e80cb22f'
auth_token = '25628f4df2124f081c048d95e9e1d98a'
client = Client(account_sid, auth_token)
PKG_STATE = ['no_pkg', 'yes_pkg']

# Setting up redis
rdsdb = redis.Redis(host='localhost',
                    port='6379',
                    password='package_thief')

@app.task
def take_img(body):
    # cli_id = int(cli_id)
    img = body['img']
    np_img = np.frombuffer(img, dtype=np.int8)
    info = json.loads(body['info'].decode('utf8'))
    shape = info['size']
    print('incoming image from : {}'.format(info['id']))
    np_img = np_img.reshape(shape)
    save_img(info['id'], np_img)
    change_pkg_state(detect(np_img), info['id'])

# Setting up detector
detector = Detector()

def save_img(house_id, img):
    img_uuid = uuid4()
    rdsdb.rpush(house_id, img_uuid)
    rdsdb.set(img_uuid, img)

def detect(img):
    score, categ = detector.detect_obj(img)
    # pprint(zip(categ, score))
    print(categ, score)
    if 'suitcase' in categ:
        return True
    else:
        return False

def change_pkg_state(obj_detected, id):
    status_str = str(id)+'_status'
    current_state = rdsdb.get(status_str).decode('ascii')
    # if no_pkg
    if current_state == '0':
        if obj_detected:
            rdsdb.set(status_str, '1')
            print('changing house {} to got package'.format(id))
    # if yes_pkg
    elif current_state == '1':
        if not obj_detected:
            rdsdb.set(status_str, '0')
            print('changing house {} to no package'.format(id))
    else:
        raise ValueError('id {} is not online in redis'.format(id))