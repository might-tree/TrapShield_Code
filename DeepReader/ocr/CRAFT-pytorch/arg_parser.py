import argparse
from config_v3_main import PATH_TO_CRAFT, \
                            IMAGES_EXTENSIONS_TO_ACCEPT,\
                            MULTI_LANGUAGE_MODEL_PATH, ENGLISH_LANGUAGE_MODEL,\
                            REFINER_MODEL, DETECTOR_TEMP_FOLDER, RESULT_FOLDER, USE_CUDA
from collections import OrderedDict
def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict
def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")
parser = argparse.ArgumentParser(description='CRAFT Text Detection')
parser.add_argument('--trained_model', default=MULTI_LANGUAGE_MODEL_PATH, type=str, help='pretrained model')
parser.add_argument('--text_threshold', default=0.7, type=float, help='text confidence threshold')
parser.add_argument('--low_text', default=0.4, type=float, help='text low-bound score')
parser.add_argument('--link_threshold', default=0.4, type=float, help='link confidence threshold')
parser.add_argument('--cuda', default=False, type=str2bool, help='Use cuda for '
                                                             'inference')
parser.add_argument('--canvas_size', default=1280, type=int, help='image size for inference')
parser.add_argument('--mag_ratio', default=1.5, type=float, help='image magnification ratio')
parser.add_argument('--poly', default=False, action='store_true', help='enable polygon type')
parser.add_argument('--show_time', default=False, action='store_true', help='show processing time')
parser.add_argument('--test_folder', default='/data/', type=str, help='folder path to input images')
parser.add_argument('--refine', default=False, action='store_true',help='enable link refiner')
parser.add_argument('--refiner_model', default=REFINER_MODEL, type=str, help='pretrained refiner model')
parser.add_argument('--result_folder', default=RESULT_FOLDER, type=str, help='folder_with output images')
args = parser.parse_known_args()[0]
#print (args)
