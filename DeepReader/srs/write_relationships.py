import os
import sys
import pdb
import pandas as pd


from data_transfer import upload_to_storage, download_from_storage

from relation_container import Relation_Container

def escape_characters(cleaned_word):
    return cleaned_word.replace("\\", " ")

def sort_on_y_box_relationship(indice, list_of_boxes):
    return list_of_boxes[indice].get_coordinates(mode=4)[1]

def sort_on_x_box_relationship(indice, list_of_boxes):
    return list_of_boxes[indice].get_coordinates(mode=4)[0]

'''
write relationship and write_box_box_relationship_to_database are used to write the relations to database
'''
def write_relationship(all_boxes, cloud, image_path, index, sorting_function, relationship_dict, relationship_file_dict, relationship):
    insert_list = []
    
    for i, a_box in enumerate(all_boxes):

        all_boxes_of_relationship = relationship_dict[i][relationship]

        all_boxes_of_relationship = sorted(all_boxes_of_relationship, key=lambda box: sorting_function(box, all_boxes))

        for j, key in enumerate(all_boxes_of_relationship):
            insert_list.append([a_box.unique_id, a_box.get_text().encode("UTF-8"), all_boxes[key].unique_id,  all_boxes[key].get_text().encode("UTF-8"), j])

    columns = ["{}_id".format(relationship_file_dict[relationship].opposite_relation),
                 "{}_text".format(relationship_file_dict[relationship].opposite_relation),
                 "{}_id".format(relationship_file_dict[relationship].relation_name), 
                 "{}_text".format(relationship_file_dict[relationship].relation_name),
                 "order_id"]
    

    dataframe = pd.DataFrame(insert_list, columns = columns)

    output_folder = os.path.join("/tmp", "output", os.path.basename(image_path)[:-4])
    #output_folder = os.path.join("/mnt/model/", "output", os.path.basename(image_path)[:-4])
    #output_folder = os.path.join("output", os.path.basename(image_path)[:-4])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    csv_path = os.path.join(output_folder, relationship_file_dict[relationship].name_to_save_with + ".tsv")
    dataframe.to_csv(csv_path, sep = "\t", mode="w")
    # write output file to cloud storage
    storage_file_name = 'srs_'+ os.path.basename(image_path)[:-4] + '_' + relationship_file_dict[relationship].name_to_save_with 
    upload_to_storage(csv_path, storage_file_name + ".tsv",cloud)
    os.remove(csv_path)
    
    json_path = os.path.join(output_folder, relationship_file_dict[relationship].name_to_save_with + ".json")
    with open(json_path, 'w') as fi:
        fi.write(dataframe.to_json())

    upload_to_storage(json_path, storage_file_name + ".json",cloud)
    os.remove(json_path)
    #return dataframe.to_json()
'''
Code for iterating over all the relationships
'''
def write_box_box_relationship(all_boxes,  cloud, image_path, index, relationship_dict = {}, relationship_file_dict ={}):
    write_relationship(all_boxes, cloud, image_path, index, sort_on_y_box_relationship, relationship_dict, relationship_file_dict, "RIGHT")
    write_relationship(all_boxes, cloud, image_path, index, sort_on_y_box_relationship, relationship_dict, relationship_file_dict, "LEFT")
    write_relationship(all_boxes,cloud,  image_path, index, sort_on_x_box_relationship, relationship_dict, relationship_file_dict, "BELOW")
    write_relationship(all_boxes,cloud,  image_path, index, sort_on_x_box_relationship, relationship_dict, relationship_file_dict, "ABOVE")
    #return {'right' : right_relations, 'left' : left_relations, 'below' : below_relations, 'above' : above_relations}
    #right_relations = write_relationship(all_boxes, cloud, image_path, index, sort_on_y_box_relationship, relationship_dict, relationship_file_dict, "RIGHT")
    #left_relations = write_relationship(all_boxes, cloud, image_path, index, sort_on_y_box_relationship, relationship_dict, relationship_file_dict, "LEFT")
    #below_relations = write_relationship(all_boxes,cloud,  image_path, index, sort_on_x_box_relationship, relationship_dict, relationship_file_dict, "BELOW")
    #above_relations = write_relationship(all_boxes,cloud,  image_path, index, sort_on_x_box_relationship, relationship_dict, relationship_file_dict, "ABOVE")
    #return {'right' : right_relations, 'left' : left_relations, 'below' : below_relations, 'above' : above_relations}

