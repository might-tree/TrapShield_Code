import json

import pandas as pd
import os
import sys
import pickle
from type_tagger import semantic_sentence_tagger
from convert_lines_to_dataframe import convert_sentences_to_dataframe
from convert_object_dataframe import convert_to_dataframe
from data_transfer import upload_to_storage, download_from_storage

def run_data_type_process(image_path, cloud, mode = "SENTENCES", log_string = "" ):
    path_to_cache = "/tmp/cache/"
    if not os.path.exists(path_to_cache):
        os.makedirs(path_to_cache)
 
    path_to_cache_file = ""
    output_file = ""
    
    if mode == "SENTENCES":
        log_string = log_string + "\nNow Processing Sentences"
        path_to_cache_file = os.path.join(path_to_cache, os.path.basename(image_path)[:-4] + "_sentence_objects.pkl")
        output_file = os.path.basename(image_path)[:-4] + "_sentence_objects.pkl"
        download_from_storage(output_file, path_to_cache + output_file,cloud)


    elif mode == "BLK":
        log_string = log_string + "\nNow Processing Text Blocks"
        path_to_cache_file = os.path.join(path_to_cache, os.path.basename(image_path)[:-4] + "_textblock_objects.pkl")
        output_file = os.path.basename(image_path)[:-4] + "_textblock_objects.pkl"
        download_from_storage(output_file, path_to_cache + output_file,cloud)

    objects = None
    with open(path_to_cache_file, "rb") as f:
        objects = pickle.load(f)
 
    objects, log_string = semantic_sentence_tagger(objects, mode, log_string)

    with open( path_to_cache_file, "wb") as f:
        pickle.dump(objects, f)

    # write file to gcp storage bucket deepreader_output
    upload_to_storage(path_to_cache_file,output_file,cloud)
    
    
    dataframe = None
    
    if mode == "SENTENCES":
        dataframe, _ = convert_sentences_to_dataframe(objects)
        #return {"lines_master" : dataframe.to_json()}, log_string
    else :
        dataframe, _ = convert_to_dataframe(objects)
        #return {"textblock_master" :dataframe.to_json()}, log_string
    os.remove(path_to_cache_file)
    return log_string
    
def data_type_handler(event,p):
    data = event['queryStringParameters'] #.get_json()
    
    # data = request.get_json() 
    image_name = data["image_name"]
    
    cloud="GCP"
    if "storage" in data:
        cloud = data["storage"]
    

    log_string = ""
    image_path = '/tmp/'+ image_name 
    data["image_path"]=image_path
    download_from_storage(image_name,image_path,cloud)
    
    index = 0

    mode = 'SENTENCES'
    if "mode" in data:
        mode = data['mode']

            
    #data_frame_converted_to_json, logstring  = run_data_type_process(image_path, mode, cloud)
    logstring  = run_data_type_process(image_path, cloud, mode )
    os.remove(image_path)
    return { 'status' : "sucess", 'logstring' : logstring}

