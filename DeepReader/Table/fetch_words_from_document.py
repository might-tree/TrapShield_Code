import numpy as np
import json
import subprocess
import os
import pandas as pd

from google.cloud import storage
client = storage.Client()
bucket_name = 'perc_bucket'
bucket = client.get_bucket(bucket_name)

def download_file_from_gcs(source, dest):
    blob = bucket.blob(source)
    blob.download_to_filename(dest)

class WordFetcher:
    def __init__(self, file_name, out_location, extract_locally = True):
        self.file = file_name
        self.output_location = out_location
        self.generate = False
        self.tesseract_dir = os.path.join(os.getcwd(), 'Vision_APIs/OCR/tesseract/')


    def generator(self):
        # call the locally installed tesseract with package
        # And save the output to the given location
#       command = str('/home/rohit/.virtualenvs/deep_reader_env/bin/python2 tesseract_class.py -f ' + self.file + ' -o ' + self.output_location)
        command = str('/home/manju/python-env/DeepReaderEnvV2/bin/python3.5 tesseract_class.py -f ' + self.file + ' -o ' + self.output_location)
        subprocess.call(command, shell=True, cwd=self.tesseract_dir)

    def fetcher(self):
        # LOGIC to fetch json file from server and save it in location
        #########################
        filename_only = str(os.path.splitext(os.path.basename(self.file))[0])
        npy_file = self.output_location +"coor_"+ str(filename_only) + ".npy"
        #path_to_server_data = os.path.join(os.getcwd(), "server_dump")
        path_to_server_data = "/tmp/server_dump"
        if not os.path.exists(path_to_server_data):
            os.mkdir(path_to_server_data)
        file_name_tb = str(filename_only) + "_textblock_master.json"
        path_to_file = os.path.join(path_to_server_data, file_name_tb )
        
        #print("path to file is : {}".format(path_to_file))
        #download_file_from_gcs(file_name_tb,path_to_file)
        
        df = pd.read_json(path_to_file)
        df = df[["w_x1", "w_y1", "w_x2", "w_y2", "word_text"]]
        to_save = df.to_numpy()
        np.save(npy_file, to_save)
        #print("saved npy file")
        pass

    def get_data(self):
        if self.generate:
            self.generator()
        else:
            self.fetcher()
        filename_only = str(os.path.splitext(os.path.basename(self.file))[0])
        npy_file = self.output_location +"coor_"+ str(filename_only) + ".npy"
        dff = np.load(npy_file, allow_pickle=True)
        return dff
