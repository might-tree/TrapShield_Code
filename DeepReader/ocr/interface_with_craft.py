#import subprocess
#import requests
import os
import time
import sys
import shutil
from config_v3_main import PATH_TO_CRAFT, \
    IMAGES_EXTENSIONS_TO_ACCEPT,\
                            MULTI_LANGUAGE_MODEL_PATH, ENGLISH_LANGUAGE_MODEL,\
                            REFINER_MODEL, DETECTOR_TEMP_FOLDER, RESULT_FOLDER, USE_CUDA
from handle_folder_or_image import get_test_folder
#sys.path.append("/home/manju/faas/deepreaderv3/CRAFT-pytorch")

sys.path.append(os.path.join(os.getcwd(), "CRAFT-pytorch"))
from test1 import inference

def run_craft_on_image(folder_or_image_path, word_or_line = "line", log_string = ""):

  if not os.path.exists(folder_or_image_path):
    print("File not present at the specified path, please check the path")
    exit()

  test_folder = get_test_folder(folder_or_image_path, DETECTOR_TEMP_FOLDER)

  if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)
  
  build_json = {
      "test_folder":test_folder,
      "trained_model":MULTI_LANGUAGE_MODEL_PATH,
      "refiner_model" : REFINER_MODEL,
      "result_folder" :RESULT_FOLDER,
      "cuda" :USE_CUDA
  }
  build_json['refine'] = False
  inference(build_json)

  return log_string

if __name__ == "__main__":
  image_folder_path = sys.argv[1]
  run_craft_on_image(image_folder_path)
