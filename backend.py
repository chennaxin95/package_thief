import hug
import argparse
import cv2
import json
import redis
import numpy as np
from uuid import uuid4
from pprint import pprint
from twilio.rest import Client
from object_detection.obj_detection import Detector

from celery import Celery

# Setting up args
parser = argparse.ArgumentParser()
parser.add_argument('--redis_host', type=str, default='127.0.0.1' ,
                    help='redis hostname')
parser.add_argument('--redis_port', type=int, default=6379 ,
                    help='redis port')
parser.add_argument('--redis_password', type=str, default='package_thief',
                    help='redis password')

args = parser.parse_args()

# SETTING UP CONSTANTS
account_sid = 'AC59f219f50e0c807bbef4a098e80cb22f'
auth_token = '25628f4df2124f081c048d95e9e1d98a'
client = Client(account_sid, auth_token)
PKG_STATE = ['no_pkg', 'yes_pkg']

# Setting up redis
rdsdb = redis.Redis(host=args.redis_host,
                    port=args.redis_port,
                    password=args.redis_password)

# Setting up detector
detector = Detector()

app = Celery('backbone', broker='redis://package_thief@localhost:6379')

@hug.post('/img_upload')
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

@hug.post('/go_online')
def admission(id):
    rdsdb.set(str(id)+'_status', '0')

@hug.get('/info')
def get_info(house_id):
    return {'house_id': house_id,
            'img_id': str(uuid4())}

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


def send_alert(body):
    call = client.messages.create(from_='+12062033943',
                                  to='+12064278603',
                                  body='Ahoy from Twilio!')
    return call

if __name__ == '__main__':
    hug.API(__name__).http.serve()