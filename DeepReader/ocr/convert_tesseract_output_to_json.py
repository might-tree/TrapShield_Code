import os
import shutil
import pandas as pd
import pdb

from Sentence import Sentence
from Word import Word
from config_v3_main import FINAL_RESULT_FOLDER
from data_transfer import upload_to_storage, download_from_storage

def create_text_blocks_master(tesseract_output_dictionary):
  df_columns = ["word_id", "word_text", "data_type", "semantic_data_type", "w_x1",\
                "w_y1", "w_x2", "w_y2", "line_id", "line_text", "l_x1", "l_y1", "l_x2", "l_y2",
                "l_x3", "l_y3", "l_x4", "l_y4", "textblock_id", "textblock_text", "tb_x1", "tb_y1",
                "tb_x2", "tb_y2"]

  rows = create_line_master(tesseract_output_dictionary, return_df=False)
  for a_row in rows:
    a_row.extend([0, "NA", 1,1,100,100])
  
  dataframe = pd.DataFrame(rows, columns=df_columns)
  return dataframe


def create_line_master(tesseract_output_dictionary, return_df = True):
  df_columns = ["word_id", "word_text", "data_type", "semantic_data_type", "w_x1",\
                "w_y1", "w_x2", "w_y2", "line_id", "line_text", "l_x1", "l_y1", "l_x2", "l_y2",
                "l_x3", "l_y3", "l_x4", "l_y4"]
  rows = []
  for i, a_sentence in enumerate(tesseract_output_dictionary):
    [l_x1, l_y1], [l_x2, l_y2], [l_x3, l_y3], [l_x4, l_y4] = a_sentence.get_coordinates(mode = 8)
    line_text = a_sentence.get_text()
        
    all_words = a_sentence.get_words()
    for j, a_word in enumerate(all_words):
      word_text = a_word.get_text()
      w_x1, w_y1, w_x2, w_y2 = a_word.get_coordinates()
      rows.append([str(j) + "_" + str(i), word_text, "<alphanumeric>", "<none>", w_x1, w_y1, w_x2, w_y2, i, line_text, 
                  l_x1, l_y1, l_x2, l_y2, l_x3, l_y3, l_x4, l_y4])
  
  if return_df :
    dataframe = pd.DataFrame(rows, columns=df_columns)
    return dataframe
  
  else:
    return rows

def convert_tess_output_to_json(tesseract_output_dictionary, cloud, log_string = ""):
  
  output_dict = {}

  for image_name in tesseract_output_dictionary:
    #print("converting {} output to json ".format(image_name))
    log_string = log_string + "converting {} output to json ".format(image_name)
    
    line_master_file = create_line_master(tesseract_output_dictionary[image_name])
    text_blocks_master_file = create_text_blocks_master(tesseract_output_dictionary[image_name])
    
    path_to_output_directory = os.path.join(FINAL_RESULT_FOLDER, os.path.splitext(image_name)[0])
    if os.path.exists(path_to_output_directory):
      shutil.rmtree(path_to_output_directory)
    os.makedirs(path_to_output_directory)
    
    path_to_line_master_file = os.path.join(path_to_output_directory, "lines_master.json")
    line_master_file.to_json(path_to_line_master_file)
    iname = os.path.splitext(image_name)[0]
    upload_to_storage(path_to_line_master_file, iname + "_sentences.json", cloud )
    
    path_to_text_blocks_master_file = os.path.join(path_to_output_directory, "text_blocks_master.json")
    text_blocks_master_file.to_json(path_to_text_blocks_master_file)
    upload_to_storage(path_to_text_blocks_master_file, iname + "_textblock_master.json", cloud )

    output_dict[image_name] = {"text_blocks_master" : text_blocks_master_file.to_json(), "lines_master" : line_master_file.to_json()}
    os.remove(path_to_line_master_file)
    os.remove(path_to_text_blocks_master_file)
    
  return output_dict, log_string
