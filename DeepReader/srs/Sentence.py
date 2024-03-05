'''
Author : Rohit Rahul
Description : This will contain the information regarding each sentence in a single object
            It will contain the polygon in the shapely Polygon object 
            It will also contain the coordinates and the text
'''
import shapely
from random import randint
import numpy as np
from shapely.geometry import Polygon
import pdb

class Sentence(object):

    def __init__(self, recognized_sentence = "", coordinates = [], polygon = []):
        self.unique_id = randint(0, 10000)
        self.coordinates = coordinates
        self.recognized_sentence = recognized_sentence
        self.polygon = self.set_coordinates(polygon)
        self.words = []


    def convert_to_four(self):
        
        if len(np.array(self.coordinates).reshape(-1)) == 8:
            x1, y1, x2, y2, x3, y3, x4, y4 = self.coordinates.reshape(-1)
            return [min(x1, x2, x3, x4), min(y1, y2, y3, y4), max(x1, x2, x3, x4), max(y1, y2, y3, y4)]
        
        else:
            return self.coordinates
    
    def get_coordinates(self, mode = 8):
        if mode == 8:
            return self.coordinates
        else:
            return self.convert_to_four()

    def get_polygon(self):
        return self.polygon

    # we assume that as input we can either get a list of coordinates or a polygon
    def set_coordinates(self, polygon_or_coordinates):
        if isinstance(polygon_or_coordinates, Polygon):
            self.polygon = polygon_or_coordinates
            int_coords = lambda x: np.array(x).round().astype(np.int32)
            self.coordinates = int_coords(polygon_or_coordinates.exterior.coords)[:-1]
        else:
            if len(polygon_or_coordinates) != 0:
                self.coordinates = polygon_or_coordinates

    def get_text(self):
        return self.recognized_sentence

    def set_text(self, sentence_recognized):
        self.recognized_sentence = sentence_recognized

    def set_words(self, words):
        if not isinstance(words, (list,)):
            words = [words]
        self.words = words

    def get_words(self):
        return self.words

    def get_sorted_words(self):
        newlist = sorted(self.words, key=lambda x: x.get_coordinates()[0], reverse=True)
        return newlist
    