import os
from glob import glob
import time
import pdb
from shapely import geometry
import numpy as np
import pickle
import sys

from config_v3_main import RESULT_FOLDER, PRE_OCR_TEMP_FOLDER, OCR_TEMP_FOLDER, DEBUG, OCR_RESULT_FOLDER
from handle_folder_or_image import get_test_folder
from read_file_coords import get_coordinates
from cut_lines_from_image import cut_lines_from_image
from fasteract import get_word_bounding_box
from Word import Word
from Sentence import Sentence
from convert_tesseract_output_to_json import convert_tess_output_to_json
from data_transfer import upload_to_storage, download_from_storage

def process_images(folder_or_image_path, cloud, log_string = ""):
  '''
  Here we are getting all the images from the specified folder
  '''
  test_folder = get_test_folder(folder_or_image_path, PRE_OCR_TEMP_FOLDER)
  all_images = glob(test_folder + "/*.png")
  all_images.extend(glob(test_folder + "/*.jpg"))

  '''
  This first loop is run when you pass multiple images/pages to the code to process
  '''
  sentence_data_all_images = {}
  json_file_all_images = {}
  for i, an_image in enumerate(all_images):
    result_path = os.path.join(RESULT_FOLDER, os.path.splitext(os.path.basename(an_image))[0] + ".txt")

    if DEBUG:
      print("\nChecking for detector result at {}".format(result_path))    
      print("\nworking on {}".format(an_image))
    log_string = log_string + "\nworking on {}".format(an_image)
    log_string = log_string + "\nChecking for detector result at {}".format(result_path)

    if os.path.exists(result_path):
      all_contents = get_coordinates(result_path)
      cut_lines_from_image(an_image, all_contents, OCR_TEMP_FOLDER)
      '''
      Here we are running OCR on each page after cropping the individual line from it
      '''
      destination_folder_path = os.path.join(OCR_TEMP_FOLDER, os.path.splitext(os.path.basename(an_image))[0])
      all_cropped_images = glob(destination_folder_path + "/*.png")
      all_words = get_word_bounding_box(all_cropped_images, ["--psm 7"])

      if DEBUG:
        print("\ncompleted running tesseract on {}".format(an_image))
      log_string = log_string + "\ncompleted running tesseract on {}".format(an_image)
      
      '''
      The second loop is for images of all the cropped words
      '''
      all_sentences_in_image = []
      for j in range(len(all_cropped_images)):
        
        # converting string to integers
        coords = [int(coord) for coord in os.path.splitext(os.path.basename(all_cropped_images[j]))[0].split("_")]
        '''
        This handles the case where we just have
        x1, y1 and x2, y2 then we will expand it 
        to be 4 coordinates otherwise shapely will
        throw up an error
        '''
        if len(coords) == 4:
          x1, y1, x2, y2 = coords
          coords = [x1, y1, x2, y1, x2, y2, x1, y2]
        
        '''
        Getting the minimum of x and y to add
        '''
        all_x = [coords[i] for i in range(0, len(coords), 2)]
        all_y = [coords[i] for i in range(1, len(coords), 2)]
        min_x, min_y = min(all_x), min(all_y)
        
        '''
        Converting coordinates for adding to Sentence object
        '''
        coords = np.array(coords).reshape(-1, 2)

        word_list = []
        recognized_sentence = ""
        # selecting jth sentence
        for a_word in all_words[j]:
          word_text = a_word.get_word().replace("|", "")
          recognized_sentence = recognized_sentence + " " + word_text
          word_coordinates = a_word.get_coordinates()
          wx1, wy1, wx2, wy2 = word_coordinates
          word_coordinates = wx1 + min_x, wy1 + min_y, wx2 + min_x, wy2 + min_y
          word_list.append(Word(word_text, word_coordinates))

        '''
        Creating the sentence object and adding all the attributes to it
        '''
        temp_sent_obj = Sentence(recognized_sentence=recognized_sentence, polygon=geometry.Polygon(coords))
        temp_sent_obj.set_words(word_list)
        all_sentences_in_image.append(temp_sent_obj)

      sentence_data_all_images[os.path.basename(an_image)] = all_sentences_in_image

      if not os.path.exists(OCR_RESULT_FOLDER):
        os.makedirs(OCR_RESULT_FOLDER)

      iname = os.path.splitext(os.path.basename(an_image))[0]
      ocr_result_path = os.path.join(OCR_RESULT_FOLDER, iname)
      with open(ocr_result_path, "wb") as f:
        pickle.dump(all_sentences_in_image, f)
        
      upload_to_storage(ocr_result_path,  iname + "_sentence_objects.pkl", cloud)
      os.remove(ocr_result_path)
    else:
      if DEBUG:
        print("\nDetector result not found at {}".format(result_path))
      log_string = log_string + "\nDetector result not found at {}".format(result_path)
  '''
  Creating the output file for the image
  '''
  if DEBUG:
    print("sentence data to convert to lines {}".format(len(sentence_data_all_images)))
  log_string = log_string + "sentence data to convert to lines {}".format(len(sentence_data_all_images))
      
  json_file_all_images, log_string = convert_tess_output_to_json(sentence_data_all_images, cloud, log_string)
  # json_file_all_images[os.path.basename(an_image)] = [text_blocks_json, lines_json]
  # print(sentence_data_all_images)
  # pdb.set_trace()
  # print (os.path.join(RESULT_FOLDER, os.path.splitext(
  #                           os.path.basename(an_image))[0]))
  list_of_files = glob(os.path.join(RESULT_FOLDER, os.path.splitext(
                            os.path.basename(an_image))[0]) +  "*")
  for i in list_of_files:
    os.remove(i)
  # print (list_of_files)
  return json_file_all_images, log_string
   

if __name__ == "__main__":
  folder_or_image = sys.argv[1]
  start_time = time.time()
  process_images(folder_or_image)
  end_time = time.time()
  print("total time taken : {} seconds".format(end_time - start_time))
  total_files = 1
  if os.path.isdir(folder_or_image):
    total_files = len(os.listdir(folder_or_image))
  print("time taken per image : {} seconds".format(float(end_time - start_time)/float(total_files)))
