import requests
import threading
import pandas as pd
import os
#from make_celery import make_celery
import pickle

# from box_box_relation_builder import Box_Spatial_Relation
# from write_relationships import write_box_box_relationship

# import sys
# #import cv2
# from PIL import Image as cv2


# # This is to import the pdf to image conversion module


# from relation_container import Relation_Container
# from data_transfer import upload_to_storage, download_from_storage

def request_task(url):
    print("threadPOST")
    requests.post(url)

# def run_spatial_rel_tagging(image_path, cloud, index, mode = "SENTENCES", log_string = ""):
#     #path_to_cache = os.path.join("/mnt/model/cache")
#     path_to_cache = "/tmp/cache/"
#     if not os.path.exists(path_to_cache):
#         os.makedirs(path_to_cache)
#     path_to_cache_file = ""
#     output_file = ""
#     result = None

#     image = cv2.open(image_path)
#     width, height = image.size
#     #height, width = image.shape[:2]

#     if mode == "SENTENCES":
#         log_string = log_string + "\nNow Processing Sentences"
#         path_to_cache_file = os.path.join(path_to_cache, os.path.basename(image_path)[:-4] + "_sentence_objects.pkl")
#         output_file = os.path.basename(image_path)[:-4] + "_sentence_objects.pkl"
#         download_from_storage(output_file, path_to_cache_file, cloud )

#         list_of_sentences = None
#         with open(path_to_cache_file, "rb") as f:
#             list_of_sentences = pickle.load(f)

#         bsr = Box_Spatial_Relation(list_of_sentences, height, width)
#         relation_dict = bsr.relation_dictionary

#         # since we are using a generic code to write the final relationships 
#         # this dictionary is telling that code what exactly to name the file where
#         # all the relations will be written
#         relationship_file_dict = {"RIGHT" : Relation_Container('RIGHT', 'LEFT', "right_line"),\
#             "LEFT" : Relation_Container('LEFT', 'RIGHT', "left_line"),\
#             "ABOVE" : Relation_Container('ABOVE', 'BELOW', "above_line"),\
#             "BELOW" : Relation_Container('BELOW', 'ABOVE', "below_line")}
    
#         result = write_box_box_relationship(list_of_sentences, cloud, image_path, index, relation_dict, relationship_file_dict)
#         os.remove(path_to_cache_file)
        
#     elif mode == "BLK":
#         log_string = log_string + "\nNow Processing Text Blocks"
#         path_to_cache_file = os.path.join(path_to_cache, os.path.basename(image_path)[:-4] + "_textblock_objects.pkl")
#         output_file = os.path.basename(image_path)[:-4] + "_textblock_objects.pkl"
#         download_from_storage(output_file, path_to_cache_file, cloud)

#         text_blocks = []
#         with open(path_to_cache_file, "rb") as f:
#                 text_blocks = pickle.load(f)
        
#         bsr = Box_Spatial_Relation(text_blocks, height, width)
#         relation_dict = bsr.relation_dictionary
#         relationship_file_dict = {"RIGHT" : Relation_Container('RIGHT', 'LEFT', "right_block"),\
#             "LEFT" : Relation_Container('LEFT', 'RIGHT', "left_block"),\
#             "ABOVE" : Relation_Container('ABOVE', 'BELOW', "above_block"),\
#             "BELOW" : Relation_Container('BELOW', 'ABOVE', "below_block")}
#         #result = write_box_box_relationship(text_blocks, cloud, image_path, index, relation_dict, relationship_file_dict)
#         write_box_box_relationship(text_blocks, cloud, image_path, index, relation_dict, relationship_file_dict)
#         os.remove(path_to_cache_file)
#     return log_string


#def inference(data):
def spatial_relation_handler(request,request2):
    
    url = "https://us-central1-hardy-order-392006.cloudfunctions.net/Honeypot"
    threading.Thread(target=request_task, args=(url,)).start()
    print("Done")
    
    # data = request.get_json(silent=True)
    # image_name = data["image_name"]
    
    # cloud="AWS"
    # if "storage" in data:
    #     cloud = data["storage"]


    # log_string = ""
        
    # image_path = '/tmp/'+ data["image_name"]
    # download_from_storage(image_name,image_path,cloud)
    
    # index = 0

    # mode = 'SENTENCES'
    # if "mode" in data:
    #     mode = data['mode']



    # log_string = run_spatial_rel_tagging(image_path, cloud, index,  mode)
    
    # os.remove(image_path)   
    
    # return {'result' : "success", "logstring": log_string}