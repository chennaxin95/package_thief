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


def sendVideoFrameRandomly():
	

def readVideoFrames(video):
	while 1: 
		vidcap = cv2.VideoCapture(video)
		success,image = vidcap.read()
		count = 0
		success = True
		while success:

			# time.sleep(5) 
			cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file  
			# use alexa to send images   
			success,image = vidcap.read()
			print('Read a new frame: ', success, count)
			count += 1


def ImageToArray(path):
	image_path = os.path.join(path)
	image = Image.open(image_path)
	return np.array(image)


def ifImageSimilar(img1, img2):
    '''
    Assume input images size are the same
    '''
    diff = abs(img1-img2)
    threshold = diff[ np.where( diff >= 1.0 ) ]
    count = len(threshold)
    return float(count)/float(img1.shape[0]*img1.shape[1])        




readVideoFrames('video.avi')


# def 