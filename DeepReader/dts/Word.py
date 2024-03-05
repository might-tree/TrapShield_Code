import shapely
from random import randint
import numpy as np
from shapely.geometry import Polygon
import pdb

class Word(object):

    def __init__(self, recognized_word = "", coordinates = [], polygon = []):
        self.unique_id = randint(0, 10000)
        #[x1, y1, x2, y2]
        self.coordinates = coordinates
        self.recognized_word = recognized_word
        self.polygon = self.set_coordinates(polygon)
        self.words = []
        
        self.data_type = 'alphanumeric'
        self.semantic_data_type = 'none'

    def get_coordinates(self):
        return self.coordinates
    
    def get_polygon(self):
        return self.polygon

    # we assume that as input we can either get a list of coordinates or a polygon
    def set_coordinates(self, polygon_or_coordinates):
        
        if isinstance(polygon_or_coordinates, Polygon):
            self.polygon = polygon_or_coordinates
            int_coords = lambda x: np.array(x).round().astype(np.int32)
            self.coordinates = int_coords(polygon_or_coordinates.exterior.coords)
        else:
            if len(polygon_or_coordinates) != 0:
                self.coordinates = polygon_or_coordinates

    def get_text(self):
        return self.recognized_word

    def set_text(self, word_recognized):
        self.recognized_word = word_recognized

    def set_datatype(self, datatype):
        self.data_type = datatype
    
    def get_datatype(self):
        return self.data_type
    
    def set_semantic_datatype(self, semantic_type):
        self.semantic_data_type = semantic_type

    def get_semantic_datatype(self):
        return self.semantic_data_type
    