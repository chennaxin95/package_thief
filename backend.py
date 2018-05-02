import hug
import argparser
import cv2
import json
import redis
import numpy as np
from uuid import uuid4
from twilio.rest import Client
from object_detection.obj_detection import detect_obj

# Setting up args
parser = argparser.ArgumentParser()
parser.add_argument('--redis_host', type=str, default='127.0.0.1' ,
                    help='redis hostname')
parser.add_argument('--redis_port', type=int, default=6379 ,
                    help='redis port')
parser.add_argument('--redis_password', type=str, default='pacakge_thief',
                    help='redis password')

args = parser.parse_args()

# SETTING UP CONSTANTS
account_sid = 'AC59f219f50e0c807bbef4a098e80cb22f'
auth_token = '25628f4df2124f081c048d95e9e1d98a'
client = Client(account_sid, auth_token)
HOME_ID_STATE = {1:'no_pkg'}
PKG_STATE = ['no_pkg', 'yes_pkg']

# Setting up redis
rdsdb = redis.Redis(host=args.redis_host,
                    port=args.redis_port,
                    password=args.redis_password)

@hug.post('/img_upload')
def take_img(body):
    # cli_id = int(cli_id)
    img = body['img']
    np_img = np.frombuffer(img, dtype=np.int8)
    info = json.loads(body['info'].decode('utf8'))
    shape = info['size']
    print(info['id'])
    np_img = np_img.reshape(shape)
    print(np_img.shape)

def send_alert(body):
    call = client.messages.create(from_='+12062033943',
                                  to='+12064278603',
                                  body='Ahoy from Twilio!')
    return call
 
def save_img(house_id, img):
    img_uuid = uuid4()
    rdsdb.set(house_id, img_uuid)
    rdsdb.set(img_uuid, img)

def detect():
    pass

def change_pkg_state(obj_detected, id):
	current_state = HOME_ID_STATE{id}
	# if no_pkg
	if current_state=='no_pkg':
		if obj_detected:
			current_state = 'yes_pkg'

    # if yes_pkg
    elif current_state == 'yes_pkg':
        if not obj_detected:
            current_state = 'no_pkg'
    else:
        raise ValueError('unknown state name.')
