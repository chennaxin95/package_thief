import argparse
import cv2
import json
import redis
import numpy as np
from uuid import uuid4
from pprint import pprint
from twilio.rest import Client
from object_detection.obj_detection import Detector
from PIL import Image
import os
from .celery import app

# SETTING UP CONSTANTS
account_sid = 'AC59f219f50e0c807bbef4a098e80cb22f'
auth_token = '25628f4df2124f081c048d95e9e1d98a'
client = Client(account_sid, auth_token)
PKG_STATE = ['no_pkg', 'yes_pkg']
CUR_DIR = os.path.join(os.getcwd(), 'data')

# Setting up redis
rdsdb = redis.Redis(host='localhost',
                    port='6379',
                    password='package_thief')

# Setting up detector
detector = Detector()

@app.task
def take_img(img, info):
    np_img = np.asarray(img).astype(np.uint8)
    shape = info['size']
    print('incoming image from : {}'.format(info['id']))
    np_img = np_img.reshape(shape)
    save_img(info['id'], np_img)
    change_pkg_state(detect(np_img), info['id'])

def save_img(house_id, img):
    img_uuid = uuid4()
    rdsdb.rpush(house_id, img_uuid)
    im = Image.fromarray(img)
    save_path = os.path.join(CUR_DIR, str(img_uuid)+'.jpg')
    im.save(save_path)
    rdsdb.set(img_uuid, save_path)

def detect(img):
    _, categ = detector.detect_obj(img)
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
            send_alert('you might have a package delivery')
    # if yes_pkg
    elif current_state == '1':
        if not obj_detected:
            rdsdb.set(status_str, '0')
            print('changing house {} to no package'.format(id))
            send_alert('package might be stolen')
    else:
        raise ValueError('id {} is not online in redis'.format(id))

def send_alert(body):
    call = client.messages.create(from_='+12062033943',
                                  to='+12064278603',
                                  body=body)
    return call