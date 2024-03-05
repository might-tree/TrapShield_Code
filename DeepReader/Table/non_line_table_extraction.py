# non-line containing table detection and Extraction
import cv2
import os
import sys
import glob
import numpy as np
from pylsd.lsd import lsd
import math
import matplotlib.pyplot as plt

def draw():
    pass

def distance(x1,y1,x2,y2):
    return math.sqrt(((x2-x1)**2) + ((y2-y1)**2))

def validate_line(lines, img):
    modes = -1  # 0 for horizontal lines, 1 for vertical lines, 2 for both lines.
    h, w = img.shape[0:2]
    print(0.2*w, 0.2*h)
    llines=[]
    for it, l in enumerate(lines):
        x1,y1,x2,y2 = [int(a) for a in l[0:4]]
        dist = distance(x1,y1,x2,y2)
        slope = math.atan2(y2-y1, x2-x1)
        # logic ** if line is not 10% of the dimension, then not prominent lines
        # horizontal lines
        # print(slope , (math.pi/-4.0), (math.pi/4.0) ,  (3*math.pi/4.0), (-3*math.pi/4.0))
        if (slope > (math.pi/-4.0) and slope < (math.pi/4.0)) or (slope > (3*math.pi/4.0)) or (slope < (-3*math.pi/4.0)):
            if dist > 0.1*w:
                print("hori", dist, x1,y1,x2,y2)
                modes = 0 if modes == -1 or modes == 0 else 2
                llines.append([x1,y1,x2,y2, 0])

        # vertical lines
        else:
            if dist > 0.1*h:
                print("vert", dist, x1,y1,x2,y2)
                modes = 1 if modes == -1 or modes == 1 else 2
                llines.append([x1,y1,x2,y2, 1])

    return llines, modes

# input is the cropped table
#input_file = "/home/shubham/shubham/POC_BU_Wise_Invoice_Copy/POC_SERVER/input_pdf_image/splash.jpg"
#input_file = "/home/shubham/shubham/POC_BU_Wise_Invoice_Copy/POC_SERVER/temp2.jpg"
#input_file = "/home/shubham/shubham/POC_BU_Wise_Invoice_Copy/POC_SERVER/input_pdf_image/shoe1_table.png"
#input_file = "/home/shubham/shubham/POC_BU_Wise_Invoice_Copy/POC_SERVER/input_pdf_image/lifestyle0.png"
img = cv2.imread(input_file)
img_bw = cv2.imread(input_file, 0)

img_bw = cv2.bitwise_not(img_bw)
img_bw = cv2.dilate(img_bw, np.ones((3,3), dtype=np.uint8), iterations=2)
img_bw = cv2.bitwise_not(img_bw)
cv2.imshow('labeled.png2', img_bw)

_, img_bw = cv2.threshold(img_bw, 254, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imshow('labeled.png23', img_bw)

lines = lsd(img_bw)
print("total :", len(lines))

dist = cv2.distanceTransform(img_bw, cv2.DIST_L2, 3)
_, dist = cv2.threshold(dist, 1, 255, cv2.THRESH_BINARY)


#cv2.imshow('labeled.png', dist)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

n_lines,modes = validate_line(lines, img_bw)
print(len(n_lines))
if modes == -1:
    print("No lines")
elif modes == 0:
    print("horizontal")
elif modes == 1:
    print("vertical")
else:
    print("Both check")

# for l in n_lines:
#     #print(l[0][0], l[0][1])
#     #print(l[0], l[1])
#     if l[4] == 1:
#         img=cv2.line(img, tuple([l[0], l[1]]), tuple([l[2], l[3]]), (255,0,0))
# cv2.imshow("ss", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img_bw = cv2.bitwise_not(img_bw)
img_x_axis = np.sum(img_bw, axis=0)
img_y_axis = np.sum(img_bw, axis=1)
print(img_bw.shape, img_x_axis.shape)

tx = np.arange(0, img_bw.shape[1], 1)
ty = np.arange(0, img_bw.shape[0], 1)

# red dashes, blue squares and green triangles
plt.plot(ty, img_y_axis, 'r--')
plt.show()
