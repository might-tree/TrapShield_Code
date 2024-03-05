import pandas as pd
#import billiard as multiprocessing
from multiprocessing.pool import ThreadPool as Pool

# Expect a single text block object
def process_textblock_parallel(input_element):
    
    # This will be returned as a list
    list_to_return = []

    tblock_id, text_block_object = input_element

    text_block_text = text_block_object.get_text()
    list_of_sentences = text_block_object.get_sentences()
    tbx1, tby1, tbx2, tby2 = text_block_object.get_coordinates()
    
    # This will iterate on sentences
    for i in range(len(list_of_sentences)):
        # list_of_sentences[i].unique_id = int(str(tblock_id) + str(i))
        sentence_text = list_of_sentences[i].get_text()
        lx1, ly1, lx2, ly2, x3, y3, x4, y4 = list_of_sentences[i].get_coordinates().reshape(-1)
        list_of_words = list_of_sentences[i].get_words()
        # Iterating on the list of words
        for j in range(len(list_of_words)):
            # list_of_words[j].unique_id =  int(str(tblock_id) + str(i) + str(j))
            word_text = list_of_words[j].get_text()
            data_type = list_of_words[j].get_datatype()
            semantic_data_type = list_of_words[j].get_semantic_datatype()
            wx1, wy1, wx2, wy2 = list_of_words[j].get_coordinates()
            list_to_return.append( [
                list_of_words[j].unique_id, word_text, data_type, semantic_data_type, wx1, wy1, wx2, wy2,
                list_of_sentences[i].unique_id, sentence_text, lx1, ly1, lx2, ly2, x3, y3, x4, y4,
                tblock_id, text_block_text, tbx1, tby1, tbx2, tby2
            ])
    return [list_to_return, text_block_object]

def convert_to_dataframe(text_block_objects):
    cols = [ "word_id", "word_text", "data_type", "semantic_data_type", "w_x1", "w_y1", "w_x2", "w_y2",
                 "line_id", "line_text", "l_x1", "l_y1", "l_x2", "l_y2", "l_x3", "l_y3", "l_x4", "l_y4",
                 "textblock_id", "textblock_text", "tb_x1", "tb_y1", "tb_x2", "tb_y2"]


    #p = multiprocessing.Pool(multiprocessing.cpu_count())
    p = Pool(2)

    all_data = p.map(process_textblock_parallel, enumerate(text_block_objects))
    p.close()
    p.join()

    block_list = []
    row_list = []
    for block_data in all_data:
        a_row, text_b_obj = block_data
        row_list = row_list + a_row
        block_list.append(text_b_obj)
    
    
    dataframe = pd.DataFrame(row_list, columns = cols)
    # including index as a column
    dataframe.index.names = ['unique_id']
    
    return dataframe, block_list
    
