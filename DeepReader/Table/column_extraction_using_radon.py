from __future__ import print_function
import os
import sys
#sys.path.append(os.path.dirname(__file__))


import cv2
from copy import deepcopy
import glob
import numpy as np
import math
import time 

V2_VERSION = False

if V2_VERSION:
    from pylsd.lsd import lsd

class Column_extraction:
    def __init__(self, img):
        # read the imgae
        if type(img) == type("string"):
            self.name = img
            self.image = cv2.imread(img)
            self.bw_image = cv2.imread(img, 0)
        else:
            self.image = deepcopy(img)
            self.bw_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        (self.w, self.h) = dim
        self.ratio = float(w)/float(self.w)
        # return the resized image
        return resized

    def get_vertical_lines_v2(self, img):   # uses LSD detector

        lines = lsd(img)


        #edges = cv2.Canny(img, 50, 150, apertureSize=3)
        #minLineLength = 100
        #maxLineGap = 10
        #lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
        coord = []
        coord_len = []
        coord_arr = [0 for i in range(self.w)]
        try:
            for i in range(len(lines)):
                #print("LINESSSSSSSSSSSSSSSSSSSSSS::", lines[i])
                x1,y1,x2,y2, = int(lines[i][0]), int(lines[i][1]), int(lines[i][2]), int(lines[i][3])
                #print(x1,y1,x2,y2,_)
                #if math.sqrt((x2-x1)**2 + (y2-y1)**2) > 50:
                slope = math.atan2(y2- y1, x2-x1)
                #print(slope)
                if (slope < -1.4 and slope > -1.7) or (slope > 1.4 and slope < 1.7):
                    line_length = math.sqrt((x2-x1)**2 + (y2-y1)**2)

                    if line_length > 10:
                        coord.append(int((x1+x2)*0.5))
                        coord_len.append(line_length)
        except:
            print("No line")

        for iters, val in enumerate(coord):
            coord_arr[val] += float(coord_len[iters])/max(coord_len)
        return np.array(coord_arr), coord

    def get_vertical_lines(self, img):      # uses the standard Hough transform
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        minLineLength = 100
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
        coord = []
        coord_arr = [0 for i in range(self.w)]
        try:
            for i in range(len(lines)):
                for x1,y1,x2,y2 in lines[i]:
                    #if math.sqrt((x2-x1)**2 + (y2-y1)**2) > 50:
                    slope = math.atan2(y2- y1, x2-x1)
                    #print(slope)
                    if (slope < -1.4 and slope > -1.7) or (slope > 1.4 and slope < 1.7):
                        if math.sqrt((x2-x1)**2 + (y2-y1)**2) > 10:
                            coord.append(int((x1+x2)*0.5))
        except:
            print("No line")

        for val in coord:
            coord_arr[val] += 1
        return np.array(coord_arr), coord

    def get_vertical_line_radon(self, img):
        length_wise = []
        kernel = np.ones((3, 3), np.uint8)
        img = cv2.dilate(cv2.bitwise_not(img), kernel, iterations=1)

        I = img - np.mean(img)
        h, w = self.img.shape[0:2]
        for i in range(w):
            length_wise.append(np.sum(img[0:h, i]))

        return np.array(length_wise)

    def find_peaks(self, array, thresh = 1.0):
        rms = 1.0 * np.sqrt(np.mean(array ** 2))
        mtx = []
        for v in array:
            if abs(v) > rms:
                mtx.append(v)
            else:
                mtx.append(0)
        return mtx

    def process(self, show=False):
        # resize the image within the reasonable size
        self.img = self.image_resize(self.image, height=800)
        self.bw_img = self.image_resize(self.bw_image, height=800)

        #threshold image after blurring
        img = cv2.medianBlur(self.bw_img, 3)
        self.th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                   cv2.THRESH_BINARY, 11, 2)

        x_coord_document = []
        win = 400
        for l in range(0, self.h, win):
            self.th3 = self.th2[l:l+win, 0:self.w]

            # get information about the hough lines/LSD
            if V2_VERSION:
                self.cols_arr, self.cols = self.get_vertical_lines_v2(self.th3)
            else:
                self.cols_arr, self.cols = self.get_vertical_lines(self.th3)

            # get information about the radon lines
            self.cols_arr_radon = self.get_vertical_line_radon(self.th3)

            # logic for extraction
            radon_hough_mult = np.multiply(self.cols_arr, self.cols_arr_radon)
            final_hybrid = self.cols_arr_radon + radon_hough_mult

            #...
            data = self.find_peaks(final_hybrid, thresh=1.0)

            # finding the x-coordinate

            x_coord = []
            for i in range(len(data)):
                if data[i] >= 255 * win:
                    x_coord.append(i)
                    cv2.line(self.th3, (i, 0), (i, 100), (0,0,0), 3)
                    # cv2.imshow("debuggg", self.th3)
                    # cv2.waitKey(0)
            x_coord_document.append(x_coord)

        checker = [0] * self.w
        for xx in x_coord_document:
            for xxx in xx:
                checker[xxx] += 1
        x_coords = []

        prev = 0
        for itr in range(len(checker)):
            if checker[itr] >= 1:
                if abs(prev-itr) < 10:
                    continue
                prev = itr
                x_coords.append(int(self.ratio*itr))
                if show:
                    cv2.line(self.img, (itr, 0), (itr, 800), (0,0,0), 2)
        if show:
            cv2.imshow("ss", self.img)
            print(x_coords)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return x_coords



# resize it to the given values
if __name__ == "__main__":
    #column = Column_extraction("temp2.jpg")
    column = Column_extraction("/home/manju/deepReader/deepreader_backend/APIs/FOLDER_TABLE_READER/output_folder/1table/1table_temp.jpg")
    local_x_coord = column.process(show=False)
    for xc in local_x_coord:
        print(xc)
