import os
import pandas as pd

def convert_tsv_to_json(file_path):
  all_lines = []
  with open(file_path) as f:
    all_lines = f.readlines()

  for i in range(len(all_lines)):
    all_lines[i] = all_lines[i].replace("\n", "")
    all_lines[i] = all_lines[i].split("\t")
  
  df = pd.DataFrame(all_lines)
  #print (df)
  return df.to_json()

if __name__ == "__main__":
  path_to_file = "/home/rohit/Downloads/IMG_20190805_162752_generated_result.csv"
  json_output = convert_tsv_to_json(path_to_file)
  print (json_output)