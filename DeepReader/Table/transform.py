### RotateCorrection takes two parameter:
## input : image file name
## debug : to either view or not the radon transform
### Two main functions which is used here and are independent
## find_angle(img) -- returns the angle(degrees), line spacing.
## rotate_image(mat, angle) -- returns the rotated iamge, angle are in degrees
## process() -- takes the n times random splitting of image and get median angle.

# -*- coding: utf-8 -*-
"""
Automatically detect rotation and line spacing of an image of text using
Radon transform
If image is rotated by the inverse of the output, the lines will be
horizontal (though they may be upside-down depending on the original image)
It doesn't work with black borders
"""
from __future__ import division, print_function

try:
  import unzip_requirements
except ImportError:
  pass
import sys
#from __future__ import division, print_function
from skimage.transform import radon
from numpy import asarray, mean, array, blackman
import numpy
from numpy.fft import rfft
#import matplotlib.pyplot as plt
from matplotlib.mlab import rms_flat
import sys
print("imports skimmage numpy matplot working")
sys.path.append('/opt/lib/')
sys.path.append('/opt/')
import cv2
from random import randint as r
#@manju
import time

try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, numpy.argmax(x))[0]
except ImportError:
    from numpy import argmax

import argparse

global input_file
global output_dir

# input formatting for the data input
parser = argparse.ArgumentParser(description='Table Extraction ')
parser.add_argument('-f','--file', help='Input image for processing', required=True)
#parser.add_argument('-o','--dir', help='Output directory for saving', required=True)
args = parser.parse_args()
input_file = str(args.file)
#output_dir = str(args.dir)
#if output_dir[-1] != '/':
#    output_dir += "/"


class RotateCorrection:
    def __init__(self, input, debug=False):
        self.img_name = input
        self.debug = debug

    def rotate_image(self, mat, angle):
      # angle in degrees

      height, width = mat.shape[:2]
      image_center = (width/2, height/2)

      rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

      abs_cos = abs(rotation_mat[0,0])
      abs_sin = abs(rotation_mat[0,1])

      bound_w = int(height * abs_sin + width * abs_cos)
      bound_h = int(height * abs_cos + width * abs_sin)

      rotation_mat[0, 2] += bound_w/2 - image_center[0]
      rotation_mat[1, 2] += bound_h/2 - image_center[1]

      rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
      return rotated_mat

    def find_angle(self, img):
        I = asarray(img)
        I = I - mean(I)  # Demean; make the brightness extend above and below zero

        if self.debug:
            plt.subplot(2, 2, 1)
            plt.imshow(I)

        # Do the radon transform and display the result
        #theta = numpy.linspace(0., 180., max(img.shape), endpoint=False)
        sinogram = radon(I)

        if self.debug:
            #plt.subplot(2, 2,    2)
            #plt.imshow(sinogram.T, aspect='auto')
            #plt.gray()
            pass

        # Find the RMS value of each row and find "busiest" rotation,
        # where the transform is lined up perfectly with the alternating dark
        # text and white lines
        r = array([rms_flat(line) for line in sinogram.transpose()])
        rotation = argmax(r)
        print(r.shape)
        print('Rotation: {:.2f} degrees'.format(90 - rotation))
        if self.debug:
            plt.axhline(rotation, color='r')

        # Plot the busy row
        row = sinogram[:, rotation]
        N = len(row)
        if self.debug:
            #plt.subplot(2, 2, 3)
            pass #plt.plot(row)

        # Take spectrum of busy row and find line spacing
        window = blackman(N)
        spectrum = rfft(row * window)
        if self.debug:
            pass #plt.plot(row * window)
        frequency = argmax(abs(spectrum))
        line_spacing = N / frequency  # pixels
        print('Line spacing: {:.2f} pixels'.format(line_spacing))

        if self.debug:
            plt.subplot(2, 2, 4)
            plt.plot(abs(spectrum))
            plt.axvline(frequency, color='r')
            plt.yscale('log')
            plt.show()

        return 90 - rotation, line_spacing

    def process(self):
        orig_img = cv2.imread(self.img_name, 0)
        img = cv2.imread(self.img_name, 0)

        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        h, w = img.shape[0:2]

        if h > 3000 or w > 3000:
            win = 1000
        elif h > 1500 or w > 1500:
            win = 500
        elif h > 800 or w > 800:
            win = 400
        elif h > 300 or w > 300:
            win = 100
        else:
            win = min(h, w)
        ang = []
        for i in range(10):
            x1, y1 = r(0, min(w, h)-win), r(0, min(w, h)-win)
            if self.debug:
                cv2.imshow("Patch", img[x1:x1+win, y1:y1+win])
                cv2.waitKey(30)
            angle, _ = self.find_angle(img[x1:x1+win, y1:y1+win])
            ang.append(angle)
        angle = numpy.median(ang)
        if abs(angle) > 5.0:
            angle = 0.0
        print("Median is: ", angle, " out of: ", ang)
        rotate = self.rotate_image(orig_img, angle)

        if self.debug:
            cv2.imshow("orig", cv2.resize(img, (0, 0), fx=0.2, fy=0.2))
            cv2.imshow("rotated", cv2.resize(rotate, (0, 0), fx=0.2, fy=0.2))
            cv2.imwrite("/home/monika/Downloads/page_bank_rewrite.png", rotate)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return rotate


rot = RotateCorrection(input=input_file, debug=False)
#@manju  to check time
start = time.time()
cv2.imwrite(input_file, rot.process())
stop = time.time()
print("time for radon transform on image : ", str(stop - start))


