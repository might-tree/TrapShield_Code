import pdb
import os
import sys
import re
sys.path.append(".")

def find_pattern(input_string, pattern, label):
    list_containing_start_and_end_points = []
    m_list=[]
    for m in re.finditer(pattern, input_string):
        m_list.append(m)

    
    for m in m_list[::-1]:
        start_point = m.start(0)
        end_point = m.end(0)
        list_containing_start_and_end_points.append([start_point, end_point])
        
    return list_containing_start_and_end_points
    
# This function will take as input all the list of points and 
# mark the labels 
def from_points_to_label(points_found_list, actual_points_list, label_list, a_sentence):
    all_words = a_sentence.get_words()
    for i, actual_point in enumerate(actual_points_list):
        # if len(points_found_list) == 0:
            # print("Nothing found for {}".format(all_words[i].get_text()))
        for j, point_found in enumerate(points_found_list):
            # case 1
            # starting point of the label lies within the word boundary
            if point_found[0] > actual_point[0] and point_found[0] < actual_point[1]:
                # print("tagging {} as {}".format(all_words[i].get_text(), label_list[j]))
                all_words[i].set_semantic_datatype(label_list[j])
            # Ending point of the word lies within the word 
            elif point_found[1] > actual_point[0] and point_found[1] < actual_point[1]:
                # print("tagging {} as {}".format(all_words[i].get_text(), label_list[j]))
                all_words[i].set_semantic_datatype(label_list[j])
            
            elif actual_point[0] > point_found[0] and point_found[1] > actual_point[1]:
                # print("tagging {} as {}".format(all_words[i].get_text(), label_list[j]))
                all_words[i].set_semantic_datatype(label_list[j])
        
            # else:
                # print("Did not find a tag for {}".format(all_words[i].get_text()))
        
    a_sentence.set_words(all_words)
    # pdb.set_trace()
    return a_sentence

# This is the main function that will be called
def tag_sentence_from_dictionary(a_sentence, dictionary):
    labels_list = []
    start_end_list = []
    
    
    all_words = a_sentence.get_words()
    # This will contain all the starting and ending points of the appended words
    sentence_string = ""
    
    word_coordinates_list = []
    start_pointer = 0
    end_pointer = 0

    for a_word in all_words:
        word_text = a_word.get_text()
        length_word = len(word_text) + 1
        if sentence_string != "":
            sentence_string = sentence_string + " " + word_text
        else:
            sentence_string = sentence_string + word_text

        end_pointer = start_pointer + length_word 
        word_coordinates_list.append((start_pointer, end_pointer))
        start_pointer = end_pointer
    
    # print ("sentence to be sent is : {}".format(sentence_string))
    
    # dictionary containing all the things that we need to tag
    for a_keyword in dictionary:
        list_containing_start_and_end_points = []
        for a_key in dictionary[a_keyword]:
            return_list = find_pattern(sentence_string, re.compile(a_key.lower()), a_keyword)
            # print ("return list is : {}".format(return_list))
            if len(return_list) != 0:
                list_containing_start_and_end_points = list_containing_start_and_end_points + return_list
        # print (a_keyword)
        # print (list_containing_start_and_end_points)
        if len(list_containing_start_and_end_points) > 0:
            for start_end_point in list_containing_start_and_end_points:
                labels_list.append(a_keyword)
                start_end_list.append(start_end_point)
    
    return from_points_to_label(start_end_list, word_coordinates_list, labels_list, a_sentence)

if __name__ == "__main__":
    pass
