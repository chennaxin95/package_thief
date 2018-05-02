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


def createVideoFeeds():
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


def detect(image):
	# score, cat = detect_obj(image)
	# print score, cat
	pass
    
    
### on MAC 
### send image if not similar to previous
def readVideoFrames(video, id):
	# while 1: 
	vidcap = cv2.VideoCapture(video)
	success,image = vidcap.read()
	count = 0
	success = True
	previous = image
	alexa = Alexa(id)
	while success:
		# print(image)
		
		# time.sleep(5) 
		# cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file  
		# detect_obj(image)
		success,image = vidcap.read()
		if success:
			# print(not ifImageSimilar(previous, image))
			# print(detect_obj(image))
			# score, cat = detect_obj(image)
			# print(score, cat)
			##### create alexa to send data
			# print(type(image))
			if not (ifImageSimilar(previous, image)):
				alexa.upload(image)
				print("uploaded")
				# cv2.imwrite("frame-%d-1.jpg" % count, previous)
				# cv2.imwrite("frame-%d-2.jpg" % count, image)
		previous = image
		# print('Read a new frame: ', success, count)
		count += 1


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


image_path = 'object_detection/test_images/image7.jpg'
image = Image.open(image_path)
detect(image_path)

readVideoFrames('video.avi', 123)
# def 