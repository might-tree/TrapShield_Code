import os


DEBUG = False
CURRENT_FOLDER = os.getcwd()

PATH_TO_CRAFT = os.path.join(CURRENT_FOLDER, "./CRAFT-pytorch")

IMAGES_EXTENSIONS_TO_ACCEPT = [".jpg", ".png"]

#MULTI_LANGUAGE_MODEL_PATH = "/home/ec2-user/CraftStudentVGG16_4_AllData19.pth"
MULTI_LANGUAGE_MODEL_PATH = "/tmp/CraftStudentVGG16_4_AllData19.pth"
ENGLISH_LANGUAGE_MODEL = os.path.join(os.path.dirname(CURRENT_FOLDER), "Models", "craft_models", "craft_ic15_20k.pth")
REFINER_MODEL = os.path.join(os.path.dirname(CURRENT_FOLDER), "Models", "craft_models", "craft_refiner_CTW1500.pth")

TMP_FOLDER="/tmp/"
RESULT_FOLDER = os.path.join(TMP_FOLDER, 'result_folder')

DETECTOR_TEMP_FOLDER = os.path.join(TMP_FOLDER, "detector_temp_folder")
PRE_OCR_TEMP_FOLDER = os.path.join(TMP_FOLDER, "pre_ocr_temp_folder")
OCR_TEMP_FOLDER = os.path.join(TMP_FOLDER, "ocr_temp_folder")
OCR_RESULT_FOLDER = os.path.join(TMP_FOLDER, "ocr_result_folder")
FINAL_RESULT_FOLDER = os.path.join(TMP_FOLDER, "final_output")
USE_CUDA = False
