import pandas as pd
#import billiard as multiprocessing
from multiprocessing.pool import ThreadPool as Pool

# Expect a single text block object
def process_sentences_parallel(input_element):
    
    # This will be returned as a list
    list_to_return = []

    sentence_id, sentence_object = input_element

    # This will iterate on sentences

    sentence_text = sentence_object.get_text()
    lx1, ly1, lx2, ly2, x3, y3, x4, y4 = sentence_object.get_coordinates().reshape(-1)
    list_of_words = sentence_object.get_words()
    # Iterating on the list of words
    for j in range(len(list_of_words)):
        word_text = list_of_words[j].get_text()
        data_type = list_of_words[j].get_datatype()
        semantic_data_type = list_of_words[j].get_semantic_datatype()
        wx1, wy1, wx2, wy2 = list_of_words[j].get_coordinates()
        list_to_return.append( [
            list_of_words[j].unique_id, word_text, data_type, semantic_data_type, wx1, wy1, wx2, wy2,
            sentence_object.unique_id, sentence_text, lx1, ly1, lx2, ly2, x3, y3, x4, y4
        ])
    return [list_to_return, sentence_object]

def convert_sentences_to_dataframe(sentence_objects):
    cols = [ "word_id", "word_text", "data_type", "semantic_data_type", "w_x1", "w_y1", "w_x2", "w_y2",
                 "line_id", "line_text", "l_x1", "l_y1", "l_x2", "l_y2", "l_x3", "l_y3", "l_x4", "l_y4",
            ]


    #p = multiprocessing.Pool(multiprocessing.cpu_count())
    p = Pool(2)
    all_data = p.map(process_sentences_parallel, enumerate(sentence_objects))
    p.close()
    p.join()

    sentence_list = []
    row_list = []
    for sent_data in all_data:
        a_row, sent_obj = sent_data
        row_list = row_list + a_row
        sentence_list.append(sent_obj)
    
    
    dataframe = pd.DataFrame(row_list, columns = cols)
    # including index as a column
    dataframe.index.names = ['unique_id']
    
    return dataframe, sentence_list
    
