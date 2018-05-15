import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
# from matplotlib import pyplot as plt
from PIL import Image

from object_detection.utils import ops as utils_ops

from object_detection.utils import label_map_util

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('object_detection','data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

tf.logging.set_verbosity(tf.logging.FATAL)

def init_model():
	opener = urllib.request.URLopener()
	opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)

class Detector():
	def __init__(self):
		# already extracted
		tf.logging.set_verbosity(tf.logging.FATAL)
		tar_file = tarfile.open(MODEL_FILE)
		for file in tar_file.getmembers():
			file_name = os.path.basename(file.name)
			if 'frozen_inference_graph.pb' in file_name:
				tar_file.extract(file, os.getcwd())

		# loading tensorflow model 
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')

		self.label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
		self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
		self.category_index = label_map_util.create_category_index(self.categories)

	def run_inference_for_single_image(self, image):
		with self.detection_graph.as_default():
			with tf.Session() as sess:
				# Get handles to input and output tensors
				ops = tf.get_default_graph().get_operations()
				all_tensor_names = {output.name for op in ops for output in op.outputs}
				tensor_dict = {}
				for key in [
					'num_detections', 'detection_boxes', 'detection_scores',
					'detection_classes', 'detection_masks']:
					tensor_name = key + ':0'
					if tensor_name in all_tensor_names:
						tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
				if 'detection_masks' in tensor_dict:
					# The following processing is only for single image
					detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
					detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
					# Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
					real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
					detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
					detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
					detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image.shape[0], image.shape[1])
					detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
					# Follow the convention by adding back the batch dimension
					tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
				image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

				# Run inference
				output_dict = sess.run(tensor_dict,feed_dict={image_tensor: np.expand_dims(image, 0)})
						# all outputs are float32 numpy arrays, so convert types as appropriate
				output_dict['num_detections'] = int(output_dict['num_detections'][0])
				output_dict['detection_classes'] = output_dict[	'detection_classes'][0].astype(np.uint8)
				output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
				output_dict['detection_scores'] = output_dict['detection_scores'][0]
				if 'detection_masks' in output_dict:
					output_dict['detection_masks'] = output_dict['detection_masks'][0]
		return output_dict

	def detect_obj(self, image_np):
		shape = image_np.shape
		if shape[0] == 3:
			image_np = np.moveaxis(image_np, 0, 2)
		# Actual detection.
		output_dict = self.run_inference_for_single_image(image_np)
		# TODO change to list
		score = output_dict['detection_scores'][0]
		cat = self.category_index[output_dict['detection_classes'][0]]['name']
		# min_score_thresh > 0.2 
		return score, cat