#import billiard as multiprocessing
import sys
import os
import config as cfg
import pickle
import pdb
from simple_data_type import assign_simple_data_type


from sentence_tagging_helper import tag_sentence_from_dictionary

def create_dictionary_from_folder(path_to_folder):
    all_files = os.listdir(path_to_folder)
    dictionary = {}
    for a_file in all_files:
        # we will only look at the files which have .txt extension
        if a_file.endswith(".txt"):
            dictionary[a_file.replace(".txt", "")] = []
            path_to_file = os.path.join(path_to_folder, a_file)
            all_words = []
            with open(path_to_file, "r") as f:
                all_words = f.readlines()
            for i in range(len(all_words)):
                all_words[i] = all_words[i].replace("\n", "")
            dictionary[a_file.replace(".txt", "")] = all_words
    return dictionary


'''
This function will recieve a single sentence from the list of sentences and each sentence will be 
assigned a perticular data type.
'''
def tag_single_sentence(single_sentence, dictionary_list):
    hardcoded_dictionary, regex_dictionary = dictionary_list
    single_sentence = tag_sentence_from_dictionary(single_sentence, regex_dictionary)
    single_sentence = tag_sentence_from_dictionary(single_sentence, hardcoded_dictionary)
    single_sentence = assign_simple_data_type(single_sentence)
    return single_sentence

'''
Author : Rohit Rahul
Description : This file contains code for tagging sentences with its corresponding data type
            and semantic data type.
'''
def process_sentences(objects, hardcoded_dictionary, regex_dictionary, log_string):
    for i, an_object in enumerate(objects):
        objects[i] = tag_single_sentence(an_object, [hardcoded_dictionary, regex_dictionary])
        all_words = an_object.get_words()
        for a_word in all_words:
            log_string = log_string + "\n{}   :   {}".format(a_word.get_text(), a_word.get_semantic_datatype())
    return objects, log_string

def semantic_sentence_tagger(objects, mode="SENTENCES", log_string = ""):
    
    # create dictionary of hardcoded words
    log_string = log_string + "\nCreating Dictionary Hardcoded"
    hardcoded_dictionary = create_dictionary_from_folder(cfg.path_to_hardcoded_entities)
    # create dictionary of regex rules
    log_string = log_string + "\nCreating Dictionary Regex"
    regex_dictionary = create_dictionary_from_folder(cfg.path_to_regex_entities)

    # if sentences are being sent then this should be executed
    if mode == "SENTENCES":
        log_string = log_string + "\nNow Processing Sentences"
        objects, log_string = process_sentences(objects, hardcoded_dictionary, regex_dictionary, log_string)
        
    # if text blocks are being sent then this would be executed
    else:
        log_string = log_string + "\nNow Processing Text Blocks"  
        for i, textblk in enumerate(objects):
            sentences = textblk.get_sentences()
            objects[i].sentences, log_string = process_sentences(sentences, hardcoded_dictionary, regex_dictionary, log_string)

    return objects, log_string


if __name__ == "__main__":
    image_path = sys.argv[1]
    mode = "SENTENCES"
    path_to_cache = os.path.join(os.path.dirname(os.getcwd()), "cache")
    path_to_cache_file = ""
    
    if mode == "SENTENCES":
        path_to_cache_file = os.path.join(path_to_cache, os.path.basename(image_path)[:-4] + "_sentence_objects.pkl")
        
    elif mode == "BLK":
        path_to_cache_file = os.path.join(path_to_cache, os.path.basename(image_path)[:-4] + "_textblock_objects.pkl")
        
    objects = None
    with open(path_to_cache_file, "rb") as f:
        objects = pickle.load(f)
    
    objects, log_string = semantic_sentence_tagger(objects, mode=mode)

    log_folder = os.path.join(os.getcwd(), "logs")
    if not(os.path.exists(log_folder)):
        os.makedirs(log_folder)
    log_file = os.path.join(log_folder, (os.path.basename(image_path)[:-4]) + ".log")

    with open(log_file, "w") as f:
        f.write(log_string)

    with open( path_to_cache_file, "wb") as f:
        pickle.dump(objects, f)

    
