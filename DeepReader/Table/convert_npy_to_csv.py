import numpy as np
import csv
from tabulate import tabulate
import argparse
import traceback
import os


global input_file
global output_dirs




# input formatting for the data input
parser = argparse.ArgumentParser(description='Table Extraction ')
parser.add_argument('-f','--file', help='Input image for processing', required=True)
parser.add_argument('-o','--dir', help='Output directory for saving', required=True)
args = parser.parse_args()
input_file = str(args.file)
output_dir = str(args.dir)
if output_dir[-1] != '/':
    output_dir += "/"

filename_only = str(os.path.splitext(os.path.basename(input_file))[0])

# load file
#Store = np.load("Menlyn Shipping Manifest1.npy")
#Store = np.load("Stock not loaded on OMS 14-08-201813.npy")
try:
    #print ("error path : {}".format(output_dir + filename_only + ".npy"))
    #shubham.set_trace()
    Store = np.load(output_dir + filename_only + ".npy", allow_pickle=True)
except Exception:
    traceback.print_exc()
    print("No tables found\n")
    # shubham.set_trace()
    
column = []

Matrix = [['' for x in range(5428)] for y in range(5428)]

itr = -1
for itt, col in enumerate(Store):
    itr += 1
    for it, c in enumerate(col):
        if len(col) <= 1:
            itr -= 1
            break
        column.append([int(c[1]), int(c[0]), c[4], itr, it])
        #print (itr, c)
    #print("")
new_col = sorted(column)
#print(min(column[:]))
chk = -1
overall = []
row = []
for c in new_col:
    #print("CCCC", c)
    if chk + 30 < c[0]:
        if chk != -1:
            overall.append(row)
            row = []
        chk = c[0]
    c[2] = (c[2]).encode('ascii','ignore').decode("ascii")
    refined_str = "".join(c[2].split())
    if refined_str == "":
        continue
    row.append([refined_str, c[3], c[4], c[1]])
    #print(c, end="\n")
overall.append(row)

#print(overall)

file = open(output_dir+filename_only+'_generated_result.csv', 'w')
mainn = []

'''
It is assumed that the table can contain 20 cols/rows at max
'''
row = ['' for x in range(20)]
for chk in overall:
    weird_boss_strings = ""
    num = 1
    if c[1] == 0 and len(c[0]) > 4:
            num = 1
    chk = sorted(chk, key=lambda x: x[3])
    for c in chk:
        sstr = "".join(c[0].split())
        if sstr != "":
            row[c[1]] += c[0] + " "

    if num == 1:
        for r in row:
            try:
                rr = str(r)
            except:
                rr = r
            #print("FOCUS HERE ::::::: ", rr)
            
            if type(rr) == "<class 'int'>":
                #file.write("\'" + rr)
                #file.write("\t")
                weird_boss_strings += "\'" + rr + "\t"
            else:
                #file.write(rr+ "\t")
                weird_boss_strings += rr + "\t"
        ##### somem filtering to remove extra trailing spaces
        weird_boss_strings = weird_boss_strings.rstrip()
        #####
        file.write(weird_boss_strings + "\n")
        mainn.append(row)
        #print("*******")
        row = ['' for x in range(50)]
#file.write("\n\n")
file.close()

main_arr = []
with open(output_dir+filename_only+'_generated_result.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tempr = []
        for r in row:
            #if len(r) != 0:
            tempr.append(r)
        main_arr.append(tempr)

# logic to generate row segmentation
row_segre_arr = np.zeros((len(main_arr),1), dtype=int)
for r_cnt, r in enumerate(main_arr):
    cnt = 0
    for c in r:
        if c != '':
            cnt += 1
    row_segre_arr[r_cnt] = cnt

#print(tabulate(main_arr))
#print(row_segre_arr)
#exit()

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

f=open(output_dir+'final_result.txt', 'a+')
fname = filename_only[0:-1] + "_" + filename_only[-1]
f.write(fname)
#

f.write(tabulate(main_arr))
f.write("\n\n\n\n")
f.close()



