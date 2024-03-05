import os
import sys
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
#from matplotlib import pyplot as plt
from copy import deepcopy
os.environ['CUDA_VISIBLE_DEVICES'] = ""
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


import argparse
#@manju
#import time

#@surya
from PIL import Image
#print("Imports success in testing.py")

#start=time.time()

global file
global output_dir

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# input formatting for the data input
parser = argparse.ArgumentParser(description='Table Extraction ')
parser.add_argument('-f','--file', help='Input image for processing', required=True)
parser.add_argument('-o','--dir', help='Output directory for saving', required=True)
parser.add_argument('-g', '--use_gpu', help="Use GPU for processing of tables", type=str2bool, default=False)
args = parser.parse_args()

if not(args.use_gpu):
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
input_file = str(args.file)
output_dir = str(args.dir)
if output_dir[-1] != '/':
	output_dir += "/"
gpu=False

#CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'frozen_inference_graph.pb'
#PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

from google.cloud import storage
client = storage.Client()
bucket_name = 'perc_bucket'
bucket = client.get_bucket(bucket_name)


def download_file_from_gcs(source, dest):
    blob = bucket.blob(source)
    blob.download_to_filename(dest)
#@surya

PATH_TO_CKPT = '/tmp/frozen_inference_graph.pb'

download_file_from_gcs(MODEL_NAME, PATH_TO_CKPT)

#s3_client = boto3.client("s3")
#BUCKET_NAME = 'layerssurya' # replace with your bucket name
#KEY = "output_table_inference_graph_v1_41747.pb"  # replace with your object key 
#s3_client.download_file(BUCKET_NAME, KEY, '/tmp/'+KEY) 
#PATH_TO_CKPT = '/tmp/output_table_inference_graph_v1_41747.pb'

#suryaend---------------------------------------------------------

#PATH_TO_CKPT = "/home/rootuser/application/project/model/faster_rcnn_resnet101_coco_2018_01_28/frozen_inference_graph.pb"

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(os.getcwd(), 'table_label_map.pbtxt')

NUM_CLASSES = 1

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detect_objects(image_np, sess, detection_graph, out_path, file_name):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    #print(boxes.shape)#, scores, classes, num_detections)
    #print(scores)
    #for b in boxes[0]:
    #    print(b)

    # Visualization of the results of a detection.
    _, numpy_ar = vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    np.save(out_path+"tab_"+file_name+".npy", numpy_ar)
    return image_np


# First test on images# First
#PATH_TO_TEST_IMAGES_DIR = '/home/rootuser/application/project/*.jpg'
#TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'POD_000{}.jpg'.format(i)) for i in range(1, 5) ]
import glob
#TEST_IMAGE_PATHS = glob.glob("object_detection/test_images/stamp/testing_stamp_del_after_use/*.pdf")
#TEST_IMAGE_PATHS = glob.glob(input_file)

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


#from PIL import Image
gpu = False

#Load a frozen TF model
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
#print("Loading Model :: done")

def handler():
    
    #input_file = event["file"]
    #output_dir = event["outdir"]

    
    TEST_IMAGE_PATHS = glob.glob(input_file)

    fault = []
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph, config=tf.ConfigProto(gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.95))) as sess:
            for image_path in TEST_IMAGE_PATHS:
                image = Image.open(image_path)
                image_np = cv2.imread(image_path)
                name_f = os.path.splitext(os.path.basename(image_path))[0]
                image_process = detect_objects(image_np, sess, detection_graph, output_dir, name_f)
                #print(image_process.shape)
                im = Image.fromarray(image_process)
                im.save(output_dir+"out_" + name_f + ".jpg")

    #@manju
    #stop=time.time()
    #print("***********time for object detection : ", str(stop - start))

 
handler()

