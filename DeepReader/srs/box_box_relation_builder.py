import numpy as np
import sys
import pdb
import os

sys.path.append(".")
sys.path.append(os.path.join("generalized_classes"))

from write_relationships import write_box_box_relationship
from relation_container import Relation_Container

# output of the get_coordinates function should be x1, y1, x2, y2
# get_range_of_coordinates and intersection_of_lists and does_condition_hold are utility functions


class Box_Spatial_Relation(object):
    def __init__(self, objects_to_process, image_height, image_width, image_path = ""):
        self.debug = False
        self.relation_dict = {}
        self.objects_to_process = objects_to_process
        self.relations = ["LEFT","RIGHT","ABOVE","BELOW"]
        self.x_intersection = 0.3
        self.y_intersection = 0.3
        
        # If you want to find all of the boxes 
        # which are below/above/left/right to a 
        # specific box in question then this should be 
        # set to false otherwise should be set to true
        self.filter_to_just_one = True
        
        self.image_path = image_path
        self.image_height = image_height
        self.image_width = image_width

        self.initialize_dict()
        self.find_all_relations()


    def find_all_relations(self):
        self.left_right_relation_finder()
        self.above_below_relation_finder()

        if self.filter_to_just_one:
            if self.debug:
                pass
                #print ("\nafter stage 1 we get : \n{}".format(self.debug_relation_code()))
            self.left_right_relation_filter()
            self.above_below_relation_filter()

    @property
    def relation_dictionary(self):
        return self.relation_dict

    def get_range_of_coordinates(self, object_to_process):
        coords = object_to_process.get_coordinates(mode=4)
        
        #print "object to process is {}".format(object_to_process.get_coordinates()[0])
        all_x_coordinates = list(range(coords[0], coords[2]))
        all_y_coordinates = list(range(coords[1], coords[3]))
        return all_x_coordinates, all_y_coordinates

    def intersection_of_lists(self, lst1, lst2):
        return set(lst1).intersection(lst2)

    def filter_boxes(self, all_boxes, to_consider_list, i, relation):
        new_list_to_assign = []
        #print "\nall_boxes {}\nconsider_list {}".format(all_boxes, to_consider_list)

        for k in range(len(to_consider_list)):
            if to_consider_list[k]:
                #print "\nentering for {}\nconsider : {}".format(k, to_consider_list[k])
                new_list_to_assign.append(all_boxes[k])
        #print ("\nnew list is {}".format(new_list_to_assign))
        # pdb.set_trace()
        self.relation_dict[i][relation] = new_list_to_assign

    # This will find out if the intersection between two list meets the threshold or not
    def does_condition_hold(self, list_1, list_2, intersection_of_lists, threshold):
        if len(list_1) < len(list_2):
            if len(intersection_of_lists) / float(len(list_1)) >= threshold:
                return True
            else:
                return False
        else:
            if len(intersection_of_lists) / float(len(list_2)) >= threshold:
                return True
            else:
                return False

    def get_y_of_the_object(self, object_indice):
        coords = self.objects_to_process[object_indice].get_coordinates(mode=4)
        return coords[1]

    def get_x_of_the_object(self, object_indice):
        coords = self.objects_to_process[object_indice].get_coordinates(mode=4)
        return coords[0]

    def initialize_dict(self):
        for i in range(0, len(self.objects_to_process)):
            self.relation_dict[i] = {}
            for value in self.relations:
                self.relation_dict[i][value] = []

    def left_right_relation_finder(self):

        for i in range(len(self.objects_to_process)):
            i_x_coordinates, i_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[i])
            # the box which is to the right should have x1 greater than x1 of the box to the left
            # this threshold is saying how far away should the x1 of the box should be if it has to be considered
            # x1 of the right box should not be considered as greater than x2 of leftbox as detection isn't always perfect
            coords = self.objects_to_process[i].get_coordinates(mode = 4)
            # setting the threshold
            threshold_width = coords[0] + 0.5 * (coords[2] - coords[0])
            
            for j in range(len(self.objects_to_process)):
                coords = self.objects_to_process[j].get_coordinates(mode=4)

                if i != j and coords[0] > threshold_width:
                    j_x_coordinates, j_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[j])

                    y_intersection_list = self.intersection_of_lists(i_y_coordinates, j_y_coordinates)

                    # if the thresholding of y holds then we append the index to the relation dict
                    if self.does_condition_hold(i_y_coordinates, j_y_coordinates, y_intersection_list, self.y_intersection):
                        self.relation_dict[i]["RIGHT"].append(j)
                        self.relation_dict[j]["LEFT"].append(i)
        if self.debug:
            pass
            # self.debug_via_image("RIGHT")
            # self.debug_via_image("LEFT")

    def left_right_relation_filter(self):
        #print ("initial relation dict is {}".format(self.relation_dict))
        for a_key in self.relation_dict:
            all_boxes_to_right = self.relation_dict[a_key]["RIGHT"]

            if len(all_boxes_to_right) <= 1:
                continue

            to_consider = [True]*len(all_boxes_to_right)

            all_boxes_to_right = sorted(all_boxes_to_right, key=self.get_x_of_the_object)
            if self.debug:
                pass
                #print "\nall_boxes to the right contains the following \n{}".format(all_boxes_to_right)
            to_consider = [True]*len(all_boxes_to_right)

            for i, indice_i in enumerate(all_boxes_to_right):
                if to_consider[i]:
                    i_x_coordinates, i_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[indice_i])

                    for j, indice_j in enumerate(all_boxes_to_right):
                        if indice_i != indice_j and to_consider[j]:
                            j_x_coordinates, j_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[indice_j])
                            y_intersection_list = self.intersection_of_lists(i_y_coordinates, j_y_coordinates)
                            if self.does_condition_hold(i_y_coordinates, j_y_coordinates, y_intersection_list, self.y_intersection):
                                to_consider[j] = False
                                #print ("\nrelation dict is {}".format(self.relation_dict))
                                #print ("\nto consider is {}".format(to_consider))
                                #print ("\nremoving ..\na_key is {}\ni is {}\nj is {}".format(a_key, indice_i, indice_j))
                                # pdb.set_trace()

                                if a_key in self.relation_dict[indice_j]["LEFT"]:
                                    self.relation_dict[indice_j]["LEFT"].remove(a_key)

            self.filter_boxes(all_boxes_to_right, to_consider, a_key, "RIGHT")

        if self.debug:
            pass
            # self.debug_via_image("RIGHT")
            # self.debug_via_image("LEFT")

    '''
    def debug_via_image(self, relation):
        if self.image_path == "":
            return 
        import cv2
        from General_Code.Display_Image import display_image
        for i, key in enumerate(self.relation_dict):
            debug_image = cv2.imread(self.image_path)
            x1, y1, x2, y2 = self.objects_to_process[key].get_coordinates(mode = 4)
            cv2.rectangle(debug_image, (x1, y1), (x2, y2), (0, 0, 255), 4)
            all_detected_boxes = self.relation_dict[key][relation]
            for j in all_detected_boxes:
                x11,y11,x22,y22 = self.objects_to_process[j].get_coordinates(mode = 4)
                cv2.rectangle(debug_image, (x11, y11), (x22, y22), (0, 255, 0), 4)
                #print ("key is {} and detected boxes are {} and j is {}".format(key, all_detected_boxes, j))
                display_image(cv2.resize(debug_image, (0, 0), fx=0.3, fy=0.3))
    '''
    def above_below_relation_finder(self):
        for i in range(len(self.objects_to_process)):
            i_x_coordinates, i_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[i])
            # the box which is below should have y1 greater than y1 of the box above
            # this threshold is saying how far away should the y1 of the box should be if it has to be considered
            # y1 of the below box should not be considered as greater than y2 of abovebox as detection isn't always perfect
            threshold_height = self.objects_to_process[i].get_coordinates(mode = 4)[1] + 0.5 * (self.objects_to_process[i].get_coordinates(mode = 4)[3] - self.objects_to_process[i].get_coordinates(mode = 4)[1])
            for j in range(len(self.objects_to_process)):

                if i != j and self.objects_to_process[j].get_coordinates(mode = 4)[1] > threshold_height:
                    j_x_coordinates, j_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[j])

                    x_intersection_list = self.intersection_of_lists(i_x_coordinates, j_x_coordinates)

                    # if the thresholding of x holds then we append the index to the relation dict
                    if self.does_condition_hold(i_x_coordinates, j_x_coordinates, x_intersection_list, self.x_intersection):
                        self.relation_dict[i]["BELOW"].append(j)
                        self.relation_dict[j]["ABOVE"].append(i)

        if self.debug:
            # self.debug_via_image("BELOW")
            pass
            # self.debug_via_image("ABOVE")

    def above_below_relation_filter(self):
        total_keys = len(self.relation_dict)
        #print("relation dict initial is : {}".format(self.relation_dict))
        for a_key in range(len(self.objects_to_process)):
            all_boxes_below = self.relation_dict[a_key]["BELOW"]

            if len(all_boxes_below) <= 1:
                continue

            all_boxes_below = sorted(all_boxes_below, key=self.get_y_of_the_object)
            if self.debug:
                pass
                #print "\nall_boxes to the right contains the following \n{}".format(all_boxes_below)
            to_consider = [True]*len(all_boxes_below)

            for i, indice_i in enumerate(all_boxes_below):
                if to_consider[i]:
                    i_x_coordinates, i_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[indice_i])

                    for j, indice_j in enumerate(all_boxes_below):
                        if indice_i != indice_j and to_consider[j]:
                            j_x_coordinates, j_y_coordinates = self.get_range_of_coordinates(self.objects_to_process[indice_j])
                            x_intersection_list = self.intersection_of_lists(i_x_coordinates, j_x_coordinates)
                            if a_key == -1:
                                pass
                                # pdb.set_trace()
                                #print (to_consider)
                            evaluated_condition = self.does_condition_hold(i_x_coordinates, j_x_coordinates, x_intersection_list, self.x_intersection) 
                            if not evaluated_condition:
                                iy1 = self.objects_to_process[indice_i].get_coordinates(mode = 4)[1]
                                jy1 = self.objects_to_process[indice_j].get_coordinates(mode = 4)[1]
                                if abs(iy1 - jy1) > self.image_height/8.0:
                                    evaluated_condition = True
                            if evaluated_condition:
                                to_consider[j] = False
                                #print ("to consider is {}".format(to_consider))
                                #print ("\nremoving ..\na_key is {}\nj is {}".format(a_key, j))
                                if a_key in self.relation_dict[indice_j]["ABOVE"]:
                                    self.relation_dict[indice_j]["ABOVE"].remove(a_key)
                                #print ("after first iteration : {}".format(self.relation_dict))
                                # pdb.set_trace()
                            # This would remove any box that lies too far 
                            
            self.filter_boxes(all_boxes_below, to_consider, a_key, "BELOW")

        #f self.debug:
            # #print ("\ntotal key before were : {}\ntotal keys after : {}\n".format(total_keys, len(self.relation_dict)))
            # #print (self.relation_dict)
            #self.debug_via_image("BELOW")
            # self.debug_via_image("ABOVE")


    def get_objects_and_relations(self):
        return self.objects_to_process, self.relation_dict

    def __str__(self):
        self.debug_relation_code()

    def debug_relation_code(self):
        return "\n{}".format(self.relation_dict)


