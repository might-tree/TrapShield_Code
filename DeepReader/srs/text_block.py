'''
Author : Rohit Rahul
Description : This will contain the information regarding each textblock in a single object
            It will contain the polygon in the shapely Polygon object 
            It will also contain the coordinates and the text
'''
import shapely
from random import randint
import numpy as np
from shapely.geometry import Polygon
import pdb

class Text_Block(object):

    def __init__(self, recognized_textblock = "", coordinates = [], polygon = []):
        self.unique_id = randint(0, 10000)
        self.coordinates = coordinates
        self.recognized_textblock = recognized_textblock
         
        self.polygon = self.set_coordinates(polygon)
        self.sentences = []

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
        return self.recognized_textblock

    def set_text(self, textblock_recognized):
        self.recognized_textblock = textblock_recognized

    def set_sentences(self, sentences):
        if not isinstance(sentences, (list,)):
            sentences = [sentences]
        self.sentences = sentences

    def get_sentences(self):
        return self.sentences

    def add_sentence(self, sentence):
        self.sentences.append(sentence)
        self.recognized_textblock += " " + sentence.get_text()     