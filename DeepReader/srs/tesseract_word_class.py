class Tesseract_Word(object):
    def __init__(self, word, coordinates, data_type="<alphanumeric>", detector = "tesseract"):
        self.word = word
        self.coordinates = coordinates
        self.data_type = data_type
        self.detector = detector

    def get_coordinates(self):
        return self.coordinates

    def get_word(self):
        return self.word

    def get_data_type(self):
        return self.data_type

    def set_detector(self, detector_name):
        self.detector = detector_name

    def get_detector(self):
        return self.detector

    def set_data_type(self, data_type):
        self.data_type = data_type
