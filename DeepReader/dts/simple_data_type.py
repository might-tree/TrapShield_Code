import os
import sys


from Word import Word
from Sentence import Sentence

def assign_simple_data_type(single_sentence):
    all_words = single_sentence.get_words()
    for i in range(len(all_words)):
        
        if all_words[i].get_text().isalpha():
             all_words[i].set_datatype("alphabets")
        
        elif all_words[i].get_text().isnumeric():
            all_words[i].set_datatype("numeric")
        
        else:
            all_words[i].set_datatype("alphanumeric")
    
    single_sentence.set_words(all_words)
    return single_sentence

if __name__ == "__main__":
        list_words = ["hello" , '12345', 'h123r']
        list_sent_obj = [] 
        for word in list_words:
            list_sent_obj.append(Word(recognized_word = word))
        sent_obj = Sentence()
        sent_obj.set_words(list_sent_obj)
        assigned_sentence = assign_simple_data_type(sent_obj)
        all_words = assigned_sentence.get_words()
        for a_word in all_words:
            print ("{} : {}".format(a_word.get_text(), a_word.get_datatype()))
