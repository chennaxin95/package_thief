'''	For prechecking frames from video feeds in the edge server.
	convert images into numpy array and preprocess it.
	Check if current frame is similar to the last frame.
	If yes, do nothing. Else, send it to backend server for 
	objection detection.

'''

import numpy as np
import cv2
import os
import time
# import Image
# from object_detection.obj_detection import detect_obj

from PIL import Image
from alexa import Alexa

# generate fake video from images 
def create_video():
	image_folder = 'images'
	video_name = 'video.avi'
	images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
	frame = cv2.imread(os.path.join(image_folder, images[0]))
	height, width, layers = frame.shape
	video = cv2.VideoWriter(video_name, -1, 1, (width,height))
	for image in images:
		for i in range(20):
			video.write(cv2.imread(os.path.join(image_folder, image)))
	cv2.destroyAllWindows()
	video.release()
	# return video


# (on alien) ummy function for detecting object
def detect(image):
	score, cat = detect_obj(image)
	return score, cat
    
    
### (on MAC) 
### send image if not similar to previous
def stream_alexa(video, id, fps=24):
	vidcap = cv2.VideoCapture(video)
	success,image = vidcap.read()
	success = True
	previous = image
	alexa = Alexa(id)
	alexa.go_online()
	count = 0
	uploads = 0
	while success:
		count += 1
		success,image = vidcap.read()
		time.sleep(1./fps)
		if success:
			if not ifImageSimilar(previous, image):
				alexa.upload_celery(image.astype(np.uint8))
				uploads += 1
		previous = image
	return count, uploads

def ImageToArray(path):
	image_path = os.path.join(path)
	image = Image.open(image_path)
	return np.array(image)

def ifImageSimilar(img1, img2):
	gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
	diff = abs(gray_img1-gray_img2)
	threshold = diff[ np.where( diff >= 1.0 ) ]
	count = len(threshold)
	return (float(count)/float(gray_img1.shape[0]*gray_img1.shape[1])<0.1)

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)