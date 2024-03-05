import os
import sys
#from pdf2image import convert_from_path
import numpy as np
import glob
import shutil
import argparse

global input_file
global output_dir

# input formatting for the data input
parser = argparse.ArgumentParser(description='Table Extraction ')
parser.add_argument('-f','--file', help='Input image for processing', required=True)
parser.add_argument('-o','--dir', help='Output directory for saving', required=True)
parser.add_argument('-d','--outfile', help='Output directory for saving', required=True)
args = parser.parse_args()
input_file = str(args.file)
output_dir = str(args.dir)
out_file = str(args.outfile)
if output_dir[-1] != '/':
    output_dir += "/"
if out_file[-1] != '/':
    out_file += "/"

file_name, ext = os.path.splitext(os.path.basename(input_file))
if ext == '.jpg':
    shutil.copy2(src=input_file, dst=output_dir+file_name+ext)
else:
    pages = convert_from_path(input_file)
    cnt = 0

    for page in pages:
        page.save(output_dir+file_name+str(cnt)+".jpg", 'JPEG')
        cnt += 1
#print("Converted images")
if os.path.exists(out_file+'final_result.txt'):
    os.remove(out_file+'final_result.txt')
f = open(out_file+'final_result.txt','w')
f.close()
if os.path.exists(out_file+file_name+'_generated_result.csv'):
    os.remove(out_file+file_name+'_generated_result.csv')
f = open(out_file+file_name+'_generated_result.csv','w')
f.close()
