import os
import sys
#sys.path.append(os.path.dirname(__file__))
from column_extraction_using_radon import Column_extraction
from fetch_words_from_document import WordFetcher
import json
import cv2
import glob
import os
import re
import numpy as np
from copy import deepcopy
import math
import argparse

global input_file
global output_dir
DEBUG= False



# input formatting for the data input
parser = argparse.ArgumentParser(description='Table Extraction ')
parser.add_argument('-f','--file', help='Input image for processing', required=True)
parser.add_argument('-o','--dir', help='Output directory for saving', required=True)
parser.add_argument('-z','--header', help='file containing a list of headers', required=False)
args = parser.parse_args()
input_file = str(args.file)
output_dir = str(args.dir)
if output_dir[-1] != '/':
    output_dir += "/"

# headers that will be used for extraction
if os.path.exists(args.header):
    with open(str(args.header), "r") as f:
        header = f.readline().split(",")
else:
    print("Using default header list")
    print ("No header file found")
font = cv2.FONT_HERSHEY_SIMPLEX

filename_only = str(os.path.splitext(os.path.basename(input_file))[0])
#print(str(filename_only))

############33 for the table data_new here: format - [x1, y1, x2, y2]
npy_file = output_dir +"tab_"+ str(filename_only) + ".npy"
npy = np.load(npy_file)

ter = []
index = 0
area = 0
ind = 0
for x1, y1, x2, y2 in npy:
    ter.append([x1, y1, x2, y2])
    if abs(y2-y1)*abs(x2-x1) > area:
        area = abs(y2-y1)*abs(x2-x1)
        index = ind
    ind += 1
ter = np.array(ter)
###########33 table code ended here

# read the image
image = cv2.imread(input_file)
img = deepcopy(image)

if DEBUG:
    print("opened main image")
    cv2.imshow("ss", image)
    cv2.waitKey(0)


############################################################################
############################################################################
###########--PATCH IN THE FUNCTION and replace file loading--##############
############################################################################
############################--  BELOW  --###################################
# load the text files: format - [x1, y1, x2, y2, string]
# npy_file = output_dir +"coor_"+ str(filename_only) + ".npy"
# dff = np.load(npy_file)
word_fetch = WordFetcher(file_name=input_file, out_location=output_dir, extract_locally = True)
dff = word_fetch.get_data()
#print(df[0])
#exit()

############################--  ABOVE  --###################################
############################################################################
###########--PATCH IN THE FUNCTION and replace file loading--##############
############################################################################
############################################################################

diction = {}
df = []
t_img = deepcopy(image)
for tr, d in enumerate(dff):
    string = d[4]
    n_string = ""
    for it, s in enumerate(string):
        if s.isalnum() or s == "." or s == ",":
            n_string += s

    df.append([d[0], d[1], d[2], d[3], n_string])


df = np.array(df)

# going through every tables
for itr, table in enumerate(ter):
    if itr == index:
        pass
    else:
        continue
    #print("TTT", table)
    x_mean = []
    y_mean = []
    arr =  []
    found = False
    for x1, y1, x2, y2, string in df:

        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        #print(x1, y1, x2, y2, string)
        if "".join(string.split()) == "|" or "".join(string.split()) == "{" or "".join(string.split()) == "}":
            continue
        cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,100), 5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(image,filter_str(string),(x1, y1), font, 2,(0,0,0),5,cv2.LINE_AA)

        arr.append([x1, y1, x2, y2, string])
        # check for matching the header with the given list of headers
        # returns the list of the header with the matched

        #string = row['description']
        #found = False
        for head in header:
            if string.lower() == head.lower():
                found = True
                ## split the table
                cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255 ), 5)

                x_mean.append(x1)
                y_mean.append(y1)
                #print(y1, string)
    if found == False:
       continue
    assert len(y_mean) == len(x_mean), "Length mis-match of table headers, throw error"
    # cropping point of table region
    # function :- f(p1, p2) = (p2.y - p1.y)**2/(p2.x - p1.x)**2 , where if p2.x-p1.x = 0, then p2.x-p1.x = a, where a = 10e-3
    # sort it using function
    sort_y_med = 10000*np.ones((len(y_mean),len(y_mean)), dtype=float)
    for srt_i in range(len(y_mean)):
        for srt_j in range(srt_i+1, len(y_mean)):
            sx1, sy1, sx2, sy2 = x_mean[srt_i], y_mean[srt_i], x_mean[srt_j], y_mean[srt_j]
            srt_diffx = sx2-sx1
            srt_diffy = sy2-sy1
            if abs(srt_diffx) == 0:
                srt_diffx = 0.001
            value_calc = (float(srt_diffy)/srt_diffx)**2
            sort_y_med[srt_i][srt_j] = value_calc
    srt_min = np.argwhere(sort_y_med == np.min(sort_y_med))


    # y_coord = int(np.median(y_mean)) # old logic for table region extraction
    y_coord = int(min(y_mean[srt_min[0][1]], y_mean[srt_min[0][0]])) # new logic of clustering headers and finding common starting
    #print("Y_coord", y_coord)
    if abs(y_coord-table[1])/float(abs(table[3]-table[1])) > 0.8:
        #print("Insuffiecient conditions met to be table")
        continue

    # outputs the cropped region having table
    n_image = img[y_coord:table[3],table[0]:table[2]]

    # filters words inside the table region
    new_arr = []
    for x1, y1, x2, y2, strings in arr:
        mx = (x1+x2)*0.5
        my = (y1+y2)*0.5
        #cv2.rectangle(n_image, (x1, y1), (x2, y2), (255,0,0), 3)
        #print(table)
        if my >= y_coord and my < table[3]:
            new_arr.append([x1, y1, x2, y2, strings])
            n_image = cv2.rectangle(n_image, (x1, y1), (x2, y2), (0,0,255), -1)


####################################################################333 TABLE logics ended (filtering words, etc)

    # hough logic
    ## Hough logic
    ###instead using new_code
    ##@manju changed the name of temp2.jpg to filenametemp.jpg
    fname= output_dir + filename_only + "_temp.jpg"
    cv2.imwrite(fname, n_image)
    #cv2.imwrite("temp2.jpg", n_image)

    # #Old logic using same python
    #@manju column extraction using python3 uncommented below  lines
    #column = Column_extraction("temp2.jpg")
    column = Column_extraction(fname)
    local_x_coord = column.process(show=False)

    # adopting with table coordinate
    vector = []
    for x in local_x_coord:
        vector.append([table[0] + x, y_coord + 0, table[0] + x, y_coord + 0])
    #** vector == coordinate of lines
    #** new_arr == coordinate of text box and strings
    x_value = []
    diff_value = []
    differ=0
    for x,_,x21,_ in vector:
        #print("X_coord", x)
        x_value.append(x)
        diff_value.append([x, abs(x1-x21)])
        #print(len(vector))
    x_value.append(0)
    x_value.append(table[2])
    diff_value.append([0, 0])
    diff_value.append([table[2], 0])

    x_value = sorted(x_value)   # thus now x_value contains the x_value of column segmenter
    diff_value = sorted(diff_value, key=lambda d: (d[0], d[1]))   # thus now x_value contains the x_value of column segmenter

    from random import randint as r

    column = []
    for i in range(0,len(x_value)-1):
        rx1, rx2 = x_value[i], x_value[i+1]

        temp_column = []
        #print("column ", rx1, rx2)
        for val in new_arr: ## checking all words to be lying inside which column
            if (val[0]+val[2])*0.5 > rx1 and (val[0]+val[2])*0.5 < rx2:
                #print(rx1, (val[0]+val[2])*0.5, " --> ", (val[0]+val[2])*0.5, rx2)
                temp_column.append([val[0], val[1], val[2], val[3], val[4]])
        column.append(temp_column)
        #print(temp_column)


    for col in column:
        color = (r(0, 255), r(0, 255), r(0, 255))
        for tcol in col:
            cv2.rectangle(img, (tcol[0], tcol[1]), (tcol[2], tcol[3]), color, 3)

    mat = [['' for x in range(1000)] for y in range(1000)]
    write = []
    for i in range(len(column)):
        for j in range(len(column[i])):
            mat[i][j] = column[i][j][4]

    #print("******************************Tables_data")

    h, w = img.shape[0:2]
    temp_img = np.zeros((h, w, 3), dtype=np.uint8)
    temp_img = cv2.bitwise_not(temp_img)

    height_wise = [1] * temp_img[0:1]
    i = 0
    Store = []
    for row in column:
        color = (r(0, 125), r(0, 125), r(0, 125))
        #color = colors[i]
        #print(color)
        i += 1
        if len(row) == 0:
            continue
        #print("Rowss", row)
        #height_wise[row[0][1]] += 1
        column = []
        for tcol in row:
            #print(tcol)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(temp_img,tcol[4],(tcol[0], tcol[1]), font, 2,color,5,cv2.LINE_AA)
            column.append(tcol)
            #cv2.rectangle(img, (tcol[0], tcol[1]), (tcol[2], tcol[3]), color, 3)

        Store.append(column)
        #print(Store)
    #print()

try:
    np.save(output_dir+filename_only+".npy", np.array(Store))
except:
    print("No tables detected")
cv2.destroyAllWindows()
