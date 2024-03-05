import boto3
from botocore.exceptions import ClientError
s3 = boto3.resource('s3')
BUCKET_NAME = 'ocrdependencies'
FOLDER='python_all'
try:
    local_file_name = '/tmp/python'
    s3.Bucket(BUCKET_NAME).download_file(FOLDER, local_file_name)
except ClientError as e:
    if e.response['Error']['Code'] != "404":
        raise


import sys
import pandas as pd
import os
import base64
import tempfile
import time
import json
from run_ocr import process_images
from data_transfer import upload_to_storage, download_from_storage

from google.cloud import storage
client = storage.Client()
bucket_name = ''
bucket = client.get_bucket(bucket_name)

def download_file_from_gcs(source, dest):
    blob = bucket.blob(source)
    blob.download_to_filename(dest)


download_file_from_gcs("CraftStudentVGG16_4_AllData19.pth","/tmp/CraftStudentVGG16_4_AllData19.pth")

###to download tesseract binaries, create directory, extract zip, set ld lib path
download_file_from_gcs("tesseract_libraries.zip","/tmp/tesseract_layer.zip")

if not os.path.exists("/tmp/tesseract_lib"):
    os.makedirs("/tmp/tesseract_lib")

from zipfile import ZipFile
with ZipFile('/tmp/tesseract_layer.zip', 'r') as zipObj:
    # Extract all the contents of zip file in different directory
    zipObj.extractall('/tmp/tesseract_lib/')

os.environ["LD_LIBRARY_PATH"]="/tmp/tesseract_lib/lib"
os.environ["TESSDATA_PREFIX"]="/tmp/tesseract_lib/tesseract/share/tessdata"


os.system("chmod +rwx /tmp/tesseract_lib/bin/tesseract")
#print("added +X")

from interface_with_craft import run_craft_on_image


def run_craft_ocr(image_path,cloud):
    log_string = ""

    craft_start_time = time.time()
    log_string = run_craft_on_image(image_path, word_or_line = "line", log_string = log_string)
    craft_end_time = time.time()

    start_time = time.time()
    json_file_all_images, log_string  = process_images(image_path, cloud, log_string= log_string)
    
    print("total time taken by craft is : {} seconds ".format(craft_end_time - craft_start_time))
    print("total time taken by OCR is : {} seconds ".format(time.time() - start_time))

    text_blocks_json, lines_master_json = json_file_all_images[os.path.splitext(os.path.basename(image_path))[0] + ".png"]["text_blocks_master"], json_file_all_images[os.path.splitext(os.path.basename(image_path))[0] + ".png"]["lines_master"]
    return log_string

def ocr_handler(request): 
    data = request.get_json();
    image_name = data["image_name"]
    
    cloud="GCP"
    if "storage" in data:
        cloud = data["storage"]
        
    log_string = ""
    
    if "image_content" in data:
        log_string = log_string + "\nFound image content in the request "
        file = tempfile.mkstemp()[1]
        image_data = data['image_content']
        image_data_decode= base64.b64decode(image_data)
        if not file.endswith(".jpg"):
            file = file + ".jpg"
        with open(file,'wb') as f:
             f.write(image_data_decode)
        data['image_path'] = file
        log_string = log_string + "temp file is {}".format(file)
    
    data["image_path"]="/tmp/"+ image_name
    image_path = data["image_path"]
    download_from_storage(image_name,image_path,cloud)
       
    index = 0
     
    languages = ["engfour"]
            
    log_string = run_craft_ocr(image_path,cloud)
    os.remove(image_path)
    return {'result' : "sucess",  'log_string' : log_string }            
